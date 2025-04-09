import asyncio
import random

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core.models import ChatCompletionClient
from dotenv import load_dotenv

from settings import llm_config


async def team_2_agents_guessing_game():
    """	
    EXERCISE: Complete the guessing game between two agents
    
    In this exercise, you will implement a number guessing game where:
    1. A random number between 1-100 is generated
    2. Two agents take turns: one tries to guess the number, the other provides feedback
    3. The game ends when the number is correctly guessed
    
    Follow the TODO comments to complete the implementation.
    """

    load_dotenv()
    randomNumber = random.randint(1, 100)

    print(f"Random number to be guessed: {randomNumber}")

    # TODO: Create an OpenAI model client using the provided configuration
    # Hint: Use ChatCompletionClient.load_component() with llm_config
    client = None  # Replace this line with your code

    # TODO: Create the guesser agent
    # This agent should have a system message that explains it's playing a guessing game
    # where it guesses a number and receives feedback (too high/too low)
    # Hint: The system message should be incorrect - the guesser should NOT know the number!
    guesser = None  # Replace this with your AssistantAgent implementation

    # TODO: Create the player agent
    # This agent should have a system message that explains it has a number in mind
    # and will provide feedback on guesses (too high/too low)
    # When the correct number is guessed, it should say 'FINISH'
    player = None  # Replace this with your AssistantAgent implementation

    # TODO: Create a termination condition that ends the game when 'FINISH' is mentioned
    # Hint: Use the TextMentionTermination class
    text_termination = None  # Replace this with your termination condition

    # TODO: Create a team with the two agents using RoundRobinGroupChat
    # The team should use the termination condition defined above
    team = None  # Replace this with your RoundRobinGroupChat implementation

    # TODO This code runs the team chat - uncomment when you're ready to test
    # async for message in team.run_stream(
    #     task="I have a number between 1-100 in my mind"
    # ):  # type: ignore
    #     if isinstance(message, TaskResult):
    #         print("Stop Reason:", message.stop_reason)
    #     else:
    #         print(message)


# This line will run your solution
asyncio.run(team_2_agents_guessing_game())
