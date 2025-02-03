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
    Simulates a guessing game between two agents using an OpenAI model client.
    The function sets up two agents: a guesser and a player. The guesser tries to 
    guess a random number between 1 and 100, while the player provides feedback 
    on whether the guess is too high, too low, or correct. The game continues 
    until the correct number is guessed, at which point the player says 'FINISH'.
    The function uses the following components:
    - `load_dotenv()`: Loads environment variables from a .env file.
    - `random.randint(1, 100)`: Generates a random number between 1 and 100.
    - `ChatCompletionClient.load_component(llm_config)`: Loads the OpenAI model client.
    - `AssistantAgent`: Represents the guesser and player agents.
    - `TextMentionTermination("FINISH")`: Defines the termination condition for the game.
    - `RoundRobinGroupChat`: Manages the interaction between the two agents.
    The function prints the random number to be guessed and the messages exchanged 
    between the agents during the game. It also prints the stop reason when the game ends.
    Returns:
        None
    """

    load_dotenv()
    randomNumber = random.randint(1, 100)

    print(f"Random number to be guessed: {randomNumber}")

    client = ChatCompletionClient.load_component(llm_config)
    # Create an OpenAI model client.

    # Create the guesser agent.
    guesser = AssistantAgent(
        "guesser",
        model_client=client,
        system_message="You are playing a game of guess-my-number. You have the "
        f"number {randomNumber} in your mind, and I will try to guess it. "
        "If I guess too high, say 'too high', if I guess too low, say 'too low'. ",
    )

    # Create the player agent.
    player = AssistantAgent(
        "player",
        model_client=client,
        system_message="I have a number in my mind, and you will try to guess it. "
        "If I say 'too high', you should guess a lower number. If I say 'too low', "
        "you should guess a higher number. If the number is guessed, say 'FINISH'.",
    )

    text_termination = TextMentionTermination("FINISH")

    # Create a team with the two agents.
    team = RoundRobinGroupChat(
        [player, guesser], termination_condition=text_termination
    )

    async for message in team.run_stream(
        task="I have a number between 1-100 in my mind"
    ):  # type: ignore
        if isinstance(message, TaskResult):
            print("Stop Reason:", message.stop_reason)
        else:
            print(message)


asyncio.run(team_2_agents_guessing_game())
