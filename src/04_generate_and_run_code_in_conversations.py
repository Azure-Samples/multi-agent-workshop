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
    This function initializes and configures a local command line code executor, a chat completion client,
    a code executor agent, and a code writer agent. It then creates a team of these agents and runs them
    in a round-robin group chat to solve a specified task. The task is to write Python code to calculate
    the 14th Fibonacci number. The function uses a console to display the stream of messages exchanged
    between the agents.
    The agents follow a specific system message guideline to suggest and execute code, handle errors,
    and verify the final answer. The process terminates when the text "FINISH" is mentioned in the chat.
    Returns:
    None
    """

    load_dotenv()
    code_writer_system_message = """You are a helpful AI assistant.
    Solve tasks using your coding and language skills.
    In the following cases, suggest python code (in a python coding block) or shell script (in a sh coding block) for the user to execute.
    1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, 
    print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to
    be solved based on your language skill, you can solve the task by yourself.
    2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly.
    Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill.
    When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the
    code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended 
    to be executed by the user.
    If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. 
    Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant.
    Check the execution result returned by the user.
    If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes.
    If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, 
    collect additional info you need, and think of a different approach to try.
    When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.
    Before finisht the entire task, run the code, verify the output, and provide the final answer.
    Reply 'FINISH' in the end when everything is done.
    """

    # Create a local command line code executor.
    # You would normally prefer to run the commands in a different venv, but for simplicity, we will run them in
    # the same environment.
    executor = LocalCommandLineCodeExecutor(
        timeout=10,  # Timeout for each code execution in seconds.
        # Use the temporary directory to store the code files.
        work_dir=generated_directory,
    )

    # Get the client for chat completion.
    client = ChatCompletionClient.load_component(llm_config)

    # It is recommended that the CodeExecutorAgent agent uses a Docker container to execute code.
    # This ensures that model-generated code is executed in an isolated environment.
    # But in this example, we will use the LocalCommandLineCodeExecutor for simplicity.
    code_executor_agent = CodeExecutorAgent(
        "code_executor_agent", code_executor=executor
    )

    # Create the code writer agent.
    code_writer_agent = AssistantAgent(
        "code_writer_agent",
        model_client=client,
        system_message=code_writer_system_message,
    )

    text_termination = TextMentionTermination("FINISH")

    team = RoundRobinGroupChat(
        [code_writer_agent, code_executor_agent],
        termination_condition=text_termination,
    )
    stream = team.run_stream(
        task="Write Python code to calculate the 14th Fibonacci number."
    )
    await Console(stream)


asyncio.run(coding_agents())
