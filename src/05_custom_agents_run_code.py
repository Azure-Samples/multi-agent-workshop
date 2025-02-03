# Slightly modified Code from https://github.com/microsoft/autogen/blob/main/python/packages/autogen-core/docs/src/user-guide/core-user-guide/design-patterns/code-execution-groupchat.ipynb

import asyncio
import re
from dataclasses import dataclass
from typing import List

from autogen_core import (
    DefaultTopicId,
    MessageContext,
    RoutedAgent,
    SingleThreadedAgentRuntime,
    default_subscription,
    message_handler,
)
from autogen_core.code_executor import CodeBlock, CodeExecutor
from autogen_core.models import (
    AssistantMessage,
    ChatCompletionClient,
    LLMMessage,
    SystemMessage,
    UserMessage,
)
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from dotenv import load_dotenv

from settings import generated_directory, llm_config


@dataclass
class Message:
    content: str


@default_subscription
class Assistant(RoutedAgent):
    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__("An assistant agent.")
        self._model_client = model_client
        self._chat_history: List[LLMMessage] = [
            SystemMessage(
                content="""Write Python script in markdown block, and it will be executed.
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
class Executor(RoutedAgent):
    def __init__(self, code_executor: CodeExecutor) -> None:
        super().__init__("An executor agent.")
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
            print(f"\n{'-' * 80}\nExecutor:\n{result.output}")
            await self.publish_message(
                Message(content=result.output), DefaultTopicId()
            )


async def coding_agents():
    """
    Asynchronous function to set up and run coding agents.
    This function performs the following steps:
    1. Loads environment variables from a .env file.
    2. Creates a local embedded runtime using SingleThreadedAgentRuntime.
    3. Loads a ChatCompletionClient component with the provided LLM configuration.
    4. Initializes a LocalCommandLineCodeExecutor with a specified timeout and working directory.
    5. Registers an Assistant agent with the runtime.
    6. Registers an Executor agent with the runtime.
    7. Starts the runtime and publishes a message to the assistant to create a plot of NVIDIA vs TSLA stock.
    Returns:
        None
    """

    load_dotenv()
    # Create an local embedded runtime.
    runtime = SingleThreadedAgentRuntime()
    client = ChatCompletionClient.load_component(llm_config)

    executor = LocalCommandLineCodeExecutor(
        timeout=60,  # Timeout for each code execution in seconds.
        # Use the temporary directory to store the code files.
        work_dir=generated_directory,
    )

    (
        await Assistant.register(
            runtime,
            "assistant",
            lambda: Assistant(client),
        ),
    )

    await Executor.register(runtime, "executor", lambda: Executor(executor))

    # Start the runtime and publish a message to the assistant.
    runtime.start()
    await runtime.publish_message(
        Message(
            "Create a plot of NVIDA vs TSLA stock returns YTD from 2024-01-01."
        ),
        DefaultTopicId(),
    )
    await runtime.stop_when_idle()


asyncio.run(coding_agents())
