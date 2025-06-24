import asyncio

from dotenv import load_dotenv


async def team_2_agents():
    """
    Simulates a conversation between two agents, Chandler and Joey, who exchange jokes.
    The function performs the following steps:
    1. Loads environment variables.
    2. Creates a AzureChatCompletion using the provided configuration.
    3. Initializes two ChatCompletionAgents, Chandler and Joey, with specific system messages.
    5. Creates a ConcurrentOrchestration/SequentialOrchestration team with the two agents.
    6. Runs the conversation task and prints the result.
    7. Resets the team for a new round of jokes and runs the conversation as a stream, printing each message.
    Returns:
        None
    """
    print("test")
    load_dotenv()
    # TODO: create or re-use the chatcompletion client (settings.py)
    client = None

    # TODO: Create the chandler agent.
    chandler_agent = None

    # TODO: Create the joey agent.
    joey_agent = None

    # TODO: Create the team of agents
    agents = []

    # TODO: Create a runtime and start it
    runtime = None

    # TODO: Create either a concurrent or sequential orchestration with the agent team
    # Start the orchestration with instructions and get the results. Print them to the console
    orchestration = None

    # Stop the runtime when idle
    await runtime.stop_when_idle()


asyncio.run(team_2_agents())
