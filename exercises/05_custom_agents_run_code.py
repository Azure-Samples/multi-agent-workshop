# EXERCISE: Implementing Custom Agents with Code Execution
# Based on: https://github.com/microsoft/autogen/blob/main/python/packages/autogen-core/docs/src/user-guide/core-user-guide/design-patterns/code-execution-groupchat.ipynb

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

        # TODO: Initialize the chat history with a SystemMessage
        # The system message should instruct the AI to:
        # - Write Python script in markdown blocks for execution
        # - Save figures to files rather than using plt.show()
        # - Include all required code within a single response
        # - Fallback to generating synthetic data if yfinance cannot pull the data
        self._chat_history: List[LLMMessage] = [
            # Your code here - create a SystemMessage with appropriate instructions
        ]

    @message_handler
    async def handle_message(
        self, message: Message, ctx: MessageContext
    ) -> None:
        # TODO: Implement the message handling logic for the Assistant
        # Your code should:
        # 1. Append the incoming message to the chat history as a UserMessage
        # 2. Get a response from the model client
        # 3. Print the response with a separator
        # 4. Add the response to the chat history as an AssistantMessage
        # 5. Publish the response message

        # Your code here
        pass


def extract_markdown_code_blocks(markdown_text: str) -> List[CodeBlock]:
    # TODO: Implement a function that extracts code blocks from markdown text
    # The function should:
    # 1. Use regex to find markdown code blocks (```language\ncode```)
    # 2. Extract the language and code content from each match
    # 3. Return a list of CodeBlock objects

    # Your code here
    return []  # Replace with your implementation


@default_subscription
class Executor(RoutedAgent):
    def __init__(self, code_executor: CodeExecutor) -> None:
        super().__init__("An executor agent.")
        self._code_executor = code_executor

    @message_handler
    async def handle_message(
        self, message: Message, ctx: MessageContext
    ) -> None:
        # TODO: Implement the message handler for the Executor agent
        # Your code should:
        # 1. Extract code blocks from the message content
        # 2. If code blocks are found, execute them using the code executor
        # 3. Print the execution result with a separator
        # 4. Publish the execution result as a message

        # Your code here
        pass


async def coding_agents():
    """
    TODO: Implement the main function that sets up and runs the coding agents.

    Your implementation should:
    1. Load environment variables from a .env file
    2. Create a SingleThreadedAgentRuntime
    3. Initialize a ChatCompletionClient with the llm_config
    4. Set up a LocalCommandLineCodeExecutor with appropriate timeout and working directory
    5. Register the Assistant agent
    6. Register the Executor agent
    7. Start the runtime
    8. Publish an initial message asking to create a plot of NVIDIA vs TSLA stock returns
    9. Stop the runtime when it becomes idle
    """

    # Your code here
    pass


# TODO: Call the coding_agents function with asyncio.run()
# asyncio.run(coding_agents())
