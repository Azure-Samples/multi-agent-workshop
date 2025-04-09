import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core.models import ChatCompletionClient
from dotenv import load_dotenv

from settings import llm_config



async def team_2_agents():
    """
    EXERCISE: Implement a conversation between two agents (Chandler and Joey) who exchange jokes.

    Complete the following tasks:
    1. Load environment variables and create a ChatCompletionClient
    2. Create two AssistantAgents with appropriate system messages
    3. Set up a termination condition for the conversation
    4. Create a RoundRobinGroupChat team with the two agents
    5. Run the conversation and display the result
    6. Reset the team and run another conversation as a stream

    Refer to the instructions in the comments for each step.
    """

    # Load environment variables
    load_dotenv()

    # TODO: Create a ChatCompletionClient using the provided llm_config
    client = None  # Replace this line with the correct implementation

    # TODO: Create the Chandler agent
    # Chandler should be an AssistantAgent with:
    # - Name: "chandler"
    # - Using the model client created above
    # - A system message describing Chandler as someone who tells short story jokes related to friends
    #   and can end the conversation after 2 jokes by saying 'FINISH'
    chandler_agent = None  # Replace this line with the correct implementation

    # TODO: Create the Joey agent
    # Joey should be an AssistantAgent with:
    # - Name: "joey"
    # - Using the model client created above
    # - A system message describing Joey as someone who responds to jokes with another joke
    #   and can end the conversation after 2 jokes by saying 'FINISH'
    joey_agent = None  # Replace this line with the correct implementation

    # TODO: Create a termination condition that ends the conversation when "FINISH" is mentioned
    text_termination = (
        None  # Replace this line with the correct implementation
    )

    # TODO: Create a RoundRobinGroupChat team with both agents and the termination condition
    team = None  # Replace this line with the correct implementation

    # TODO: Run the conversation with the initial task "Start the conversation" and print the result
    result = None  # Replace this line with the correct implementation
    print(result)

    print("##################### New round as stream #####################")

    # TODO: Reset the team for a new round of jokes
    # Replace this line with the correct implementation

    # TODO: Run the conversation as a stream with the initial task "Please start the round with a joke."
    # and print each message
    # Replace these lines with the correct implementation for streaming messages
    # Hint: Use an async for loop to iterate through the stream
    # Remember to handle both TaskResult and regular message types


asyncio.run(team_2_agents())
