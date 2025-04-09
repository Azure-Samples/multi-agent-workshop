import asyncio

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core.models import ChatCompletionClient
from dotenv import load_dotenv

from settings import llm_config


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
    # Load environment variables
    load_dotenv()

    # TODO: Create a ChatCompletionClient using the provided LLM configuration
    client = None  # Replace with proper client initialization

    # TODO: Initialize the AssistantAgent with the created client
    assistant = None  # Replace with proper AssistantAgent initialization

    # TODO: Initialize the UserProxyAgent to get user input from the console
    user_proxy = None  # Replace with proper UserProxyAgent initialization

    # TODO: Create a termination condition that ends the conversation when the user says "APPROVE"
    termination = None  # Replace with proper termination condition

    # TODO: Create a RoundRobinGroupChat team with the assistant and user proxy agents
    team = None  # Replace with proper team initialization

    # TODO: Run the conversation and stream to the console
    # The task is to write a summary about the biggest news from 2025-02-03 about "deepseek"
    # If information is not available, the assistant should respond that it cannot surf the internet
    stream = None  # Replace with proper stream initialization

    # Stream the conversation to the console
    await Console(stream)


asyncio.run(human_in_the_loop())
