import asyncio

from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core.models import ChatCompletionClient
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from dotenv import load_dotenv

from settings import generated_directory, llm_config


async def coding_agents():
    """
    EXERCISE: Building Coding Agents

    In this exercise, you'll implement a system with two agents that can write and execute code:
    1. A code writer agent that proposes Python code solutions
    2. A code executor agent that runs the proposed code

    Your task is to:
    - Create a system message for the code writer agent
    - Set up a local command line executor
    - Create the necessary agents
    - Configure a round-robin team for the agents to collaborate
    - Implement a termination condition
    
    The goal is to have these agents solve a coding task (calculating the 14th Fibonacci number)
    through collaboration.
    """

    load_dotenv()
    
    # TODO: Create a system message for the code writer agent
    # The system message should instruct the agent to:
    # - Solve tasks using coding and language skills
    # - Suggest Python code or shell scripts when needed
    # - Handle errors and fix code when execution fails
    # - Verify results before finishing
    # - Reply with "FINISH" when the task is complete
    code_writer_system_message = """
    # Your system message here
    # Provide clear instructions for the code writer agent
    """

    # TODO: Create a local command line code executor
    # Configure it with an appropriate timeout and working directory
    executor = None  # Replace with actual executor implementation

    # Get the client for chat completion
    client = ChatCompletionClient.load_component(llm_config)

    # TODO: Create the code executor agent
    # This agent should use the executor you created above
    code_executor_agent = None  # Replace with actual agent implementation

    # TODO: Create the code writer agent
    # This agent should use the system message defined earlier
    code_writer_agent = None  # Replace with actual agent implementation

    # TODO: Implement a termination condition
    # The conversation should terminate when "FINISH" is mentioned
    text_termination = None  # Replace with actual termination condition

    # TODO: Create a team with round-robin chat
    # The team should include both agents and use the termination condition
    team = None  # Replace with actual team implementation

    # Run the team with a task to calculate the 14th Fibonacci number
    # The Console will display the stream of messages
    stream = team.run_stream(
        task="Write Python code to calculate the 14th Fibonacci number."
    )
    await Console(stream)


# TODO Uncomment to run the exercise
# asyncio.run(coding_agents())
