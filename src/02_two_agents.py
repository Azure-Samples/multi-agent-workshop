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
    Simulates a conversation between two agents, Chandler and Joey, who exchange jokes.
    The function performs the following steps:
    1. Loads environment variables.
    2. Creates a ChatCompletionClient using the provided configuration.
    3. Initializes two AssistantAgents, Chandler and Joey, with specific system messages.
    4. Sets up a termination condition where the conversation ends after "FINISH" is mentioned.
    5. Creates a RoundRobinGroupChat team with the two agents and the termination condition.
    6. Runs the conversation task and prints the result.
    7. Resets the team for a new round of jokes and runs the conversation as a stream, printing each message.
    Returns:
        None
    """

    load_dotenv()
    client = ChatCompletionClient.load_component(llm_config)
    # Create an OpenAI model client.

    # Create the chandler agent.
    chandler_agent = AssistantAgent(
        "chandler",
        model_client=client,
        system_message="""Your name is Chandler, and you live with Joey. You are a specialist in telling short story 
        jokes related to friends. You also hear jokes from Joey, after 2 jokes you can finish the conversation saying 
        'FINISH'.""",
    )

    # Create the joey agent.
    joey_agent = AssistantAgent(
        "joey",
        model_client=client,
        system_message="""Your name is Joey, and you live with Chandler. You listen to jokes and answer with another joke. "
        After hearing 2 jokes, you can finish the conversation saying 'FINISH'.""",
    )

    # Joey should finalize the conversation after 2 jokes of Chandler.
    text_termination = TextMentionTermination("FINISH")

    # Create a team with the primary and critic agents.
    team = RoundRobinGroupChat(
        [chandler_agent, joey_agent], termination_condition=text_termination
    )
    result = await team.run(task="Start the conversation")
    print(result)

    # Lets go for another round. But this time, as a stream.

    print("##################### New round as stream #####################")
    await team.reset()  # Reset the team for a new round of jokes.

    async for message in team.run_stream(
        task="Please start the round with a joke."
    ):  # type: ignore
        if isinstance(message, TaskResult):
            print("Stop Reason:", message.stop_reason)
        else:
            print(message)


asyncio.run(team_2_agents())
