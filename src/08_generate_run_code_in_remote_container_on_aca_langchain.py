import asyncio
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from autogen_core import (
    DefaultTopicId,
    MessageContext,
    RoutedAgent,
    SingleThreadedAgentRuntime,
    default_subscription,
    message_handler,
)
from autogen_core.code_executor import CodeBlock, CodeExecutor, CodeResult
from autogen_core.models import (
    AssistantMessage,
    LLMMessage,
    SystemMessage,
    UserMessage,
)
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from langchain_azure_dynamic_sessions import SessionsPythonREPLTool


@dataclass
class Message:
    content: str


class RemoteExecutor(CodeExecutor):
    """
    A code executor that runs code blocks in a remote Azure Container Apps instance.
    This allows for secure execution in an isolated environment with appropriate resources.

    Requirements for ACA ingress configuration:
    1. Your ACA container must have ingress enabled with an external endpoint
    2. The endpoint should be HTTPS for production use
    3. IP restrictions should be configured if needed for security
    4. Authentication should be enabled (API key is used in this code)
    """

    def __init__(
        self,
        timeout: Optional[int] = 60,
        pool_management_endpoint: Optional[str] = None,
        additional_session_config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize the RemoteExecutor with connection details for Azure Container Apps.

        Args:
            timeout: Maximum time in seconds to wait for code execution
            pool_management_endpoint: Endpoint for the Azure Container Apps session pool
            additional_session_config: Additional configuration parameters for the session
        """
        super().__init__()
        self.timeout = timeout

        # Get the pool management endpoint from environment variable if not provided
        self.pool_management_endpoint = (
            pool_management_endpoint
            or os.environ.get(
                "ACA_POOL_MANAGEMENT_ENDPOINT"
            )
        )

        # Additional configuration parameters for the session
        self.additional_session_config = additional_session_config or {}

    async def execute_code_blocks(
        self, code_blocks: List[CodeBlock], cancellation_token=None
    ) -> CodeResult:
        """
        Execute a list of code blocks in the remote Azure Container Apps instance.

        Args:
            code_blocks: List of CodeBlock objects to execute
            cancellation_token: Optional token for cancellation

        Returns:
            CodeResult with execution output and status
        """
        # Initialize logs to collect execution results
        logs = []
        exit_code = 0

        try:
            # Create a tool to interact with the remote Python REPL
            tool = SessionsPythonREPLTool(
                pool_management_endpoint=self.pool_management_endpoint,
                timeout=self.timeout,
                **self.additional_session_config,
            )

            # Execute each code block in sequence
            for i, code_block in enumerate(code_blocks):
                try:
                    # Log which block is being executed
                    block_header = f"\n--- Executing code block {i + 1}/{len(code_blocks)} ---\n"
                    logs.append(block_header)

                    # Execute the code in the remote session
                    result = tool.invoke(code_block.code)

                    # Append the result to logs
                    logs.append(result)
                except Exception as e:
                    # If execution fails, log the error and set exit code to failure
                    error_msg = (
                        f"Error executing code block {i + 1}: {str(e)}\n"
                    )
                    logs.append(error_msg)
                    exit_code = 1
                    break

            # Combine all logs into a single string
            log_output = "".join(logs)

            # Return the combined result
            return CodeResult(exit_code=exit_code, output=log_output)

        except Exception as e:
            # Handle any errors in setting up the remote execution
            return CodeResult(
                exit_code=1,
                output=f"Failed to execute code in remote container: {str(e)}",
            )


def extract_markdown_code_blocks(markdown_text: str) -> List[CodeBlock]:
    pattern = re.compile(r"```(?:\s*([\w\+\-]+))?\n([\s\S]*?)```")
    matches = pattern.findall(markdown_text)
    code_blocks: List[CodeBlock] = []
    for match in matches:
        language = match[0].strip() if match[0] else ""
        code_content = match[1]
        code_blocks.append(CodeBlock(code=code_content, language=language))
    return code_blocks


@default_subscription
class Assistant(RoutedAgent):
    def __init__(self, model_client: AzureOpenAIChatCompletionClient) -> None:
        super().__init__("An assistant agent.")
        self._model_client = model_client
        self._chat_history: List[LLMMessage] = [
            SystemMessage(
                content="""Write Python script in markdown block, and it will be executed in a remote container.
                        Always save figures to file in the current directory. Do not use plt.show().
                        All code required to complete this task must be contained within a single response.""",
            )
        ]

    @message_handler
    async def handle_message(
        self, message: Message, ctx: MessageContext
    ) -> None:
        self._chat_history.append(
            UserMessage(content=message.content, source="user")
        )
        result = await self._model_client.create(self._chat_history)
        print(f"\n{'-' * 80}\nAssistant:\n{result.content}")
        self._chat_history.append(
            AssistantMessage(content=result.content, source="assistant")
        )  # type: ignore
        await self.publish_message(
            Message(content=result.content), DefaultTopicId()
        )  # type: ignore


@default_subscription
class Executor(RoutedAgent):
    def __init__(self, code_executor: CodeExecutor) -> None:
        super().__init__("A remote executor agent.")
        self._code_executor = code_executor

    @message_handler
    async def handle_message(
        self, message: Message, ctx: MessageContext
    ) -> None:
        code_blocks = extract_markdown_code_blocks(message.content)
        if code_blocks:
            result = await self._code_executor.execute_code_blocks(
                code_blocks, cancellation_token=ctx.cancellation_token
            )
            print(f"\n{'-' * 80}\nRemote Executor:\n{result.output}")
            await self.publish_message(
                Message(content=result.output), DefaultTopicId()
            )


async def run_remote_coding_agents():
    """
    Asynchronous function to set up and run coding agents with remote execution.
    This function runs code in an Azure Container Apps instance for secure execution.
    """

    load_dotenv()
    # Create an local embedded runtime.
    runtime = SingleThreadedAgentRuntime()
    
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
    client = AzureOpenAIChatCompletionClient(
        model="gpt-4o",
        api_version="2024-06-01",
        azure_endpoint=os.environ.get("AZURE_OPENAI_URL", ""),
        azure_ad_token_provider=token_provider,
    )

    # Create the remote executor with appropriate settings
    executor = RemoteExecutor(
        timeout=60,  # Timeout for each code execution in seconds
        additional_session_config={
            "session_options": {
                "keep_alive": True,  # Keep the session alive between code blocks
                "memory_gb": 4,  # Allocate 4GB of memory to the session
                "cpu_count": 2,  # Allocate 2 CPUs to the session
            },
        },
    )

    # Register the assistant agent
    await Assistant.register(
        runtime,
        "assistant",
        lambda: Assistant(client),
    )

    # Register the executor agent that uses the remote executor
    await Executor.register(runtime, "executor", lambda: Executor(executor))

    # Start the runtime and publish a message to the assistant
    runtime.start()
    await runtime.publish_message(
        Message("Write Python code to calculate the 14th Fibonacci number."),
        DefaultTopicId(),
    )
    await runtime.stop_when_idle()


if __name__ == "__main__":
    asyncio.run(run_remote_coding_agents())
