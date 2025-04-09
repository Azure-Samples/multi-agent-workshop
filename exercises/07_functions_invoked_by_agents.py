import asyncio
from typing import Annotated, Literal

from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from autogen_core.models import ChatCompletionClient
from dotenv import load_dotenv

from settings import llm_config

# Define the operator type for our calculator function
OPERATOR = Literal["+", "-", "*", "/"]


# TODO: Implement the calculator function that performs basic arithmetic operations
# This function should take two integers and an operator, and return the result
# The operator can be "+", "-", "*", or "/"
def calculator(
    a: int, b: int, operator: Annotated[OPERATOR, "operator"]
) -> int:
    # Your implementation here:
    # 1. Check which operator is provided
    # 2. Perform the corresponding arithmetic operation
    # 3. Return the result as an integer
    # 4. For division, make sure to return an integer result

    pass  # Replace this with your implementation


def get_time() -> str:
    """
    Returns a fixed time as a string.

    Returns:
        str: A fixed time in the format "HH:MM:SS"
    """
    return "12:00:00"


async def main() -> None:
    """
    Main function to run the assistant agent.
    This function loads environment variables, initializes the ChatCompletionClient,
    and sets up the AssistantAgent with specified tools and configurations. It then
    enters a loop to continuously take user input, process it through the assistant,
    and print the assistant's response. The loop exits when the user inputs "exit".

    Your task:
    - Complete the AssistantAgent setup
    - Configure the agent to use the calculator tool

    Returns:
        None
    """

    load_dotenv()
    client = ChatCompletionClient.load_component(llm_config)

    # TODO: Initialize the AssistantAgent with proper configuration
    # 1. Give your agent an appropriate name
    # 2. Write a system message that instructs the agent to use the calculator tool
    # 3. Set up the model client
    # 4. Add the calculator and get_time functions to the tools list
    # 5. Configure whether the agent should reflect on tool use
    assistant = AssistantAgent(
        name="",  # Choose an appropriate name
        system_message="",  # Write a proper system message
        model_client=client,
        tools=[],  # Add your calculator function here and also the get_time function
        reflect_on_tool_use=False,  # Decide whether the agent should reflect on tool use
    )

    # This loop handles the conversation with the user
    while True:
        user_input = input("User: ")
        if user_input == "exit":
            break

        # TODO: Process the user input and get the assistant's response
        # 1. Send the user message to the assistant
        # 2. Get the response from the assistant
        response = await assistant.on_messages(
            # Create a TextMessage with the user's input
            [],  # Replace with appropriate message
            CancellationToken(),
        )

        # Print the assistant's response
        print("Assistant responds:", response.chat_message.content)


# Run the main function when the script is executed
if __name__ == "__main__":
    asyncio.run(main())
