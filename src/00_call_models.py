import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_core.models import ChatCompletionClient
from autogen_core.models import SystemMessage, UserMessage


from dotenv import load_dotenv

from settings import llm_config


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

    # Alternative way to initialize the model client
    # client = AzureOpenAIChatCompletionClient(
    #     model="gpt-4o",
    #     api_version="2024-06-01",
    #     azure_endpoint=os.environ.get("AZURE_OPENAI_URL", ""),
    #     api_key=os.environ.get("AZURE_OPENAI_API_KEY", ""),
    # )

    client = ChatCompletionClient.load_component(llm_config)
    
    result = await client.create([SystemMessage(content="You are a comedian specialized in telling short story jokes."), 
                                  UserMessage(content="Tell me a joke", source="user")])
    print(result)


asyncio.run(main())
