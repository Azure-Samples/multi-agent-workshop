import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_core.models import SystemMessage, UserMessage
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

from dotenv import load_dotenv

async def main():
    """
    Main asynchronous function to initialize the model client and generate a joke.
    This function performs the following steps:
    1. Loads environment variables from a .env file.
    2. Initializes the model client using Azure DefaultAzureCredential for authentication.
    3. Sends a request to the model client to generate a joke.
    4. Prints the result.
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
    
    result = await client.create([SystemMessage(content="You are a comedian specialized in telling short story jokes."), 
                                  UserMessage(content="Tell me a joke", source="user")])
    print(result)


asyncio.run(main())
