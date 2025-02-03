import asyncio
from typing import Annotated, Literal

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_core.models import ChatCompletionClient
from dotenv import load_dotenv

from settings import llm_config

OPERATOR = Literal["+", "-", "*", "/"]


def calculator(
    a: int, b: int, operator: Annotated[OPERATOR, "operator"]
) -> int:
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        return int(a / b)
    else:
        raise ValueError("Invalid operator")


async def main() -> None:
    """
    Main function to run the assistant agent.
    This function loads environment variables, initializes the ChatCompletionClient,
    and sets up the AssistantAgent with specified tools and configurations. It then
    enters a loop to continuously take user input, process it through the assistant,
    and print the assistant's response. The loop exits when the user inputs "exit".
    Returns:
        None
    """

    load_dotenv()
    client = ChatCompletionClient.load_component(llm_config)

    assistant = AssistantAgent(
        name="assistant",
        system_message="""You are a helpful assistant. For math operations, you always call your 'calculator' tool,"
        "and to get current time, you call the 'get_time' tool. You cant chat about anything else.""",
        model_client=client,
        tools=[calculator],
        reflect_on_tool_use=False,  # Set to True to have the model reflect on the tool use, set to False to return the tool call result directly.
    )
    while True:
        user_input = input("User: ")
        if user_input == "exit":
            break
        response = await assistant.on_messages(
            [TextMessage(content=user_input, source="user")],
            CancellationToken(),
        )
        print("Assistant responds:", response.chat_message.content)


asyncio.run(main())
