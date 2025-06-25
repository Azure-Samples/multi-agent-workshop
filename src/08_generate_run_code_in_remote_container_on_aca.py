# Using Semantic Kernel AgentGroupChat to facilitate communication between agents
# for remote code execution in Azure Container Apps
#


import asyncio
import datetime
import os
import re
from typing import Any, Dict, List, Optional

import dotenv
from azure.core.exceptions import ClientAuthenticationError
from azure.identity import DefaultAzureCredential
from semantic_kernel.agents import AgentGroupChat, ChatCompletionAgent
from semantic_kernel.agents.agent import Agent
from semantic_kernel.contents import ChatHistory
from semantic_kernel.core_plugins.sessions_python_tool.sessions_python_plugin import (
    SessionsPythonTool,
)
from semantic_kernel.exceptions.function_exceptions import (
    FunctionExecutionException,
)

import settings

dotenv.load_dotenv()

pool_management_endpoint = os.getenv("ACA_POOL_MANAGEMENT_ENDPOINT")


def extract_markdown_code_blocks(markdown_text: str) -> List[Dict[str, str]]:
    """Extract code blocks from markdown text."""
    pattern = re.compile(r"```(?:\s*([\w\+\-]+))?\n([\s\S]*?)```")
    matches = pattern.findall(markdown_text)
    code_blocks = []
    for match in matches:
        language = match[0].strip() if match[0] else "python"
        code_content = match[1]
        code_blocks.append({"code": code_content, "language": language})
    return code_blocks


def auth_callback_factory(scope):
    auth_token = None

    async def auth_callback() -> str:
        """Auth callback for the SessionsPythonTool.
        This is a sample auth callback that shows how to use Azure's DefaultAzureCredential
        to get an access token.
        """
        nonlocal auth_token
        current_utc_timestamp = int(
            datetime.datetime.now(datetime.timezone.utc).timestamp()
        )

        if not auth_token or auth_token.expires_on < current_utc_timestamp:
            credential = DefaultAzureCredential()

            try:
                auth_token = credential.get_token(scope)
            except ClientAuthenticationError as cae:
                err_messages = getattr(cae, "messages", [])
                raise FunctionExecutionException(
                    f"Failed to retrieve the client auth token with messages: {' '.join(err_messages)}"
                ) from cae

        return auth_token.token

    return auth_callback


class RemoteCodeExecutor:
    """
    A code executor that runs code blocks in a remote Azure Container Apps instance.
    This allows for secure execution in an isolated environment with appropriate resources.

    Requirements for ACA ingress configuration:
    1. Your ACA container must have ingress enabled with an external endpoint
    2. The endpoint should be HTTPS for production use
    3. IP restrictions should be configured if needed for security
    4. Authentication should be enabled (API key is used in this code)
    """

    def __init__(self, pool_management_endpoint: Optional[str] = None) -> None:
        """
        Initialize the RemoteCodeExecutor with connection details for Azure Container Apps.

        Args:
            timeout: Maximum time in seconds to wait for code execution
            pool_management_endpoint: Endpoint for the Azure Container Apps session pool
            additional_session_config: Additional configuration parameters for the session
        """

        # Get the pool management endpoint from environment variable if not provided
        self.pool_management_endpoint = (
            pool_management_endpoint
            or os.environ.get(
                "ACA_POOL_MANAGEMENT_ENDPOINT",
                "<TODO: Set your Azure Container Apps session pool endpoint in environment variables>",
            )
        )

    async def execute_code_blocks(
        self, code_blocks: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Execute a list of code blocks in the remote Azure Container Apps instance.

        Args:
            code_blocks: List of dictionaries with 'code' and 'language' keys

        Returns:
            Dictionary with execution output and status
        """
        # Initialize logs to collect execution results
        logs = []
        exit_code = 0

        try:
            # Create a tool to interact with the remote Python REPL

            sessions_tool = SessionsPythonTool(
                pool_management_endpoint=self.pool_management_endpoint,
                auth_callback=auth_callback_factory(
                    "https://dynamicsessions.io/.default"
                ),
                # You can also pass other parameters like:
                # env_file_path=".env",  # if you have a custom .env file
                # token_endpoint="https://your-custom-endpoint.com",  # for custom auth
            )

            # Execute each code block in sequence
            for i, code_block in enumerate(code_blocks):
                try:
                    # Log which block is being executed
                    block_header = f"\n--- Executing code block {i + 1}/{len(code_blocks)} ---\n"
                    logs.append(block_header)

                    # Execute the code in the remote session
                    result = await sessions_tool.execute_code(
                        code_block["code"]
                    )

                    # Append the result to logs
                    logs.append(str(result))
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
            return {"exit_code": exit_code, "output": log_output}

        except Exception as e:
            # Handle authentication or connection errors gracefully
            if (
                "DefaultAzureCredential" in str(e)
                or "authentication" in str(e).lower()
            ):
                return {
                    "exit_code": 1,
                    "output": f"Authentication required for remote execution. Please configure Azure credentials or run in a properly authenticated environment.\nOriginal error: {str(e)}",
                }
            else:
                # Handle any other errors in setting up the remote execution
                return {
                    "exit_code": 1,
                    "output": f"Failed to execute code in remote container: {str(e)}",
                }


async def create_code_executor_agent(
    remote_executor: RemoteCodeExecutor,
) -> Agent:
    """Create an agent specialized in executing Python code remotely."""
    kernel = settings.setup_kernel_with_chat_completion_service(
        service_id="remote-code-execution-service"
    )

    # Create agent description
    description = """I am a Remote Code Execution Agent. 
    I execute Python code in a remote Azure Container Apps instance for secure execution.
    When I receive code blocks in markdown format, I extract them and execute them remotely.
    I always report the execution results including any output or errors.
    I focus on executing code and providing execution results.
    """

    # Create the agent using ChatCompletionAgent
    code_executor_agent = ChatCompletionAgent(
        name="RemoteExecutor",
        description=description,
        kernel=kernel,
    )

    # Store the remote executor as an attribute for use in the conversation
    code_executor_agent._remote_executor = remote_executor

    return code_executor_agent


async def create_assistant_agent() -> Agent:
    """Create an assistant agent that generates Python code."""
    kernel = settings.setup_kernel_with_chat_completion_service(
        service_id="assistant-service"
    )

    # Create agent description
    description = """I am a Python Code Generation Assistant. 
    I write Python scripts in markdown code blocks that will be executed in a remote container.
    I always save figures to file in the current directory and never use plt.show().
    All code required to complete a task must be contained within a single response.
    When asked to write code, I provide it in properly formatted markdown code blocks.
    I ask @RemoteExecutor to execute the code after I provide it.
    """

    # Create the agent using ChatCompletionAgent
    assistant_agent = ChatCompletionAgent(
        name="Assistant",
        description=description,
        kernel=kernel,
    )

    return assistant_agent


async def main():
    """
    Main function to set up and run coding agents with remote execution.
    This function runs code in an Azure Container Apps instance for secure execution.
    """

    remote_executor = RemoteCodeExecutor()

    # Create the agents
    assistant_agent = await create_assistant_agent()
    executor_agent = await create_code_executor_agent(remote_executor)

    # Set up the initial chat history
    chat_history = ChatHistory()
    chat_history.add_system_message(
        "You are a team working together to generate and execute Python code remotely. "
        "The Assistant will write code, and the RemoteExecutor will execute it in a secure remote environment."
    )

    # Add the user's request
    user_request = "Write Python code to calculate the 14th Fibonacci number."
    chat_history.add_user_message(user_request)

    print(f"User: {user_request}")
    print("\n--- Starting remote coding session ---\n")

    # Create an agent group chat
    group_chat = AgentGroupChat(
        agents=[assistant_agent, executor_agent], chat_history=chat_history
    )

    # Track messages to handle code execution
    message_count = 0
    max_iterations = 6  # Limit iterations to prevent infinite loops
    code_executed = False

    # Process the conversation
    async for message in group_chat.invoke():
        message_count += 1

        # Access the name attribute directly
        agent_name = (
            message.name if hasattr(message, "name") else "Unknown Agent"
        )

        # Get the message content
        content = ""
        if hasattr(message, "content"):
            content = message.content
        elif hasattr(message, "items") and message.items:
            for item in message.items:
                if hasattr(item, "text") and item.text:
                    content += item.text

        # Print the message with agent name
        print(f"\n{'-' * 80}")
        print(f"[{agent_name}]: {content}")

        # If this is from the Assistant and contains code blocks, execute them
        if (
            agent_name == "Assistant"
            and "```" in content
            and not code_executed
        ):
            code_blocks = extract_markdown_code_blocks(content)
            if code_blocks:
                print(f"\n{'-' * 80}")
                print("Executing code remotely...")

                # Execute the code blocks
                execution_result = await remote_executor.execute_code_blocks(
                    code_blocks
                )

                print("Remote Execution Result:")
                print(f"Exit Code: {execution_result['exit_code']}")
                print(f"Output:\n{execution_result['output']}")

                code_executed = True

                # If execution was successful, we can stop here
                if execution_result["exit_code"] == 0:
                    print("\n--- Code executed successfully! ---")
                    break

        # Break if we've had enough iterations or if code was executed successfully
        if message_count >= max_iterations:
            print(f"\n--- Reached maximum iterations ({max_iterations}) ---")
            break

    print("\n--- Remote coding session completed ---\n")


if __name__ == "__main__":
    asyncio.run(main())
