# This example demonstrates how to create a Semantic Kernel agent with multiple function plugins.
# The agent can perform calculator operations and report a fixed time using native functions.
# It uses the Semantic Kernel agent framework instead of AutoGen.

import asyncio
from typing import Annotated, Literal

import dotenv
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.functions import kernel_function

import settings

dotenv.load_dotenv()

OPERATOR = Literal["+", "-", "*", "/"]


class CalculatorPlugin:
    """Plugin for performing basic calculator operations."""

    @kernel_function(
        description="Performs basic math operations (add, subtract, multiply, divide)",
        name="calculate",
    )
    def calculate(
        self,
        a: int,
        b: int,
        operator: Annotated[OPERATOR, "operator (+, -, *, /)"],
    ) -> str:
        """
        Performs basic arithmetic operations.

        Args:
            a: First number
            b: Second number
            operator: Math operation to perform (+, -, *, /)

        Returns:
            The result of the calculation as a string
        """
        if operator == "+":
            return str(a + b)
        elif operator == "-":
            return str(a - b)
        elif operator == "*":
            return str(a * b)
        elif operator == "/":
            return str(int(a / b))
        else:
            raise ValueError("Invalid operator")


class TimePlugin:
    """Plugin that returns the time."""

    @kernel_function(
        description="Returns a fixed time (12:00:00)", name="get_time"
    )
    def get_time(self) -> str:
        """
        Returns a fixed time as a string.

        Returns:
            A fixed time in the format "HH:MM:SS"
        """
        return "12:00:00"


async def main():
    """
    Main function to run the assistant agent with Semantic Kernel.
    This function initializes the Kernel, sets up the chat service,
    and creates an agent with calculator and time plugins. It then
    enters a loop to continuously take user input, process it through
    the assistant, and print the assistant's response. The loop exits
    when the user inputs "exit".
    """
    # Create the kernel and set up the chat service
    kernel = settings.setup_kernel_with_chat_completion_service(
        service_id="math-time-assistant"
    )

    # Create and register plugins
    calculator_plugin = CalculatorPlugin()
    time_plugin = TimePlugin()

    # Create the agent with the plugins
    agent = ChatCompletionAgent(
        kernel=kernel,
        name="MathTimeAssistant",
        instructions="You are a helpful assistant. For math operations, you always call your 'calculate' function, "
        "and to get current time, you call the 'get_time' function. You can't chat about anything else.",
        plugins=[calculator_plugin, time_plugin],
    )

    # Initial thread is None
    thread: ChatHistoryAgentThread | None = None

    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break

        # Invoke the agent for a response
        response = await agent.get_response(messages=user_input, thread=thread)
        print(f"Assistant: {response}")
        thread = response.thread

    # Clean up the thread
    if thread:
        await thread.delete()


if __name__ == "__main__":
    asyncio.run(main())
