import asyncio
import os

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

async def human_in_the_loop():
    """
    Facilitates a human-in-the-loop interaction between an assistant agent and a user proxy agent.
    This function sets up and runs a conversation between an AI assistant and a user proxy,
    allowing for human input via the console. The conversation continues until the user
    mentions the termination keyword "APPROVE".
    Steps:
    1. Load environment variables.
    2. Create a ChatCompletionClient using the provided LLM configuration.
    3. Initialize the AssistantAgent with the created client.
    4. Initialize the UserProxyAgent to get user input from the console.
    5. Set up a termination condition that ends the conversation when the user says "APPROVE".
    6. Create a RoundRobinGroupChat team with the assistant and user proxy agents.
    7. Run the conversation and stream the output to the console.
    The conversation task is to write a summary about the biggest news from 2025-02-03
    about "deepseek". If the information is not available, the assistant should respond
    that it cannot surf the internet to find this.
    Returns:
        None
    """

    # Create the agents.
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
    
    assistant = AssistantAgent("assistant", model_client=client)
    user_proxy = UserProxyAgent(
        "user_proxy", input_func=input
    )  # Use input() to get user input from console.

    # Create the termination condition which will end the conversation when the user says "APPROVE".
    termination = TextMentionTermination("APPROVE")

    # Create the team.
    team = RoundRobinGroupChat(
        [assistant, user_proxy], termination_condition=termination
    )

    # Run the conversation and stream to the console.
    stream = team.run_stream(
        task="Write a summary about the biggest news from 2025-02-03 about deepseek, if you can't find information just say I cant surf the internet to find this."
    )
    # Use asyncio.run(...) when running in a script.
    await Console(stream)


asyncio.run(human_in_the_loop())
