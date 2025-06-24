import asyncio

from dotenv import load_dotenv
from semantic_kernel.connectors.ai.open_ai import (
    OpenAIChatPromptExecutionSettings,
)
from semantic_kernel.contents.chat_history import ChatHistory

from settings import chat_completion_service_client


async def main():
    """
    Main asynchronous function to initialize the model client and generate a joke.
    This function performs the following steps:
    1. Loads environment variables from a .env file.
    2. Initializes the model client using a configuration.
    3. Sends a request to the model client to generate a joke.
    4. Prints the result.
    Returns:
        None
    """

    load_dotenv()

    history = ChatHistory()
    user_input = "Tell me a short story joke about a cat and a dog."

    history.add_user_message(user_input)

    execution_settings = OpenAIChatPromptExecutionSettings()
    response = await chat_completion_service_client.get_chat_message_content(
        history, settings=execution_settings
    )
    print(f"Assistant: {response}")


asyncio.run(main())
