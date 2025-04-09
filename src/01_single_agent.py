import asyncio
import os
from time import sleep

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

async def simple_agent():
    """
    Main function to run the chatbot.
    This function loads environment variables, initializes a ChatCompletionClient
    using a provided configuration, creates an AssistantAgent with a specific role,
    and runs a task to get a joke from the chatbot.
    Returns:
        None
    """

    load_dotenv()

    # Get a token credential provider using DefaultAzureCredential
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
    client = AzureOpenAIChatCompletionClient(
        model="gpt-4o",
        api_version="2024-06-01",
        azure_endpoint=os.environ.get("AZURE_OPENAI_URL", ""),
        azure_ad_token_provider=token_provider,
    )

    chatbot = AssistantAgent(
        name="chatbot",
        description="A test chatbot.",
        system_message="You are a comedian specialized in telling short story jokes.",
        model_client=client,
    )

    ## You can also use the run() method that calls on_messages() internally
    response = await chatbot.on_messages(
        [TextMessage(content="Tell me a joke", source="user")],
        CancellationToken(),
    )

    # Agent/s thought process. It gets populated when the agent is thinking, or when using tools.
    # For this example can be empty
    print(f" Touthg process: {response.inner_messages}")

    # Agent/s final response
    print(f" Agent's final response: {response.chat_message}")

    # An example with streaming messages, the Console print the messages as they appear.
    print(
        "Lets now print the messages as they appear, answering a request to tell a joke about fruits"
    )
    sleep(5)
    await Console(
        chatbot.on_messages_stream(
            [
                TextMessage(
                    content="Tell me another joke, but about fruits.",
                    source="user",
                )
            ],
            cancellation_token=CancellationToken(),
        )
    )


asyncio.run(simple_agent())
