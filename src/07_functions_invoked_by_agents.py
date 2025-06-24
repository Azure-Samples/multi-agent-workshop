# This example demonstrates how to create a Semantic Kernel agent with multiple function plugins.
# The agent can perform calculator operations and report a fixed time using native functions.
# It uses the Semantic Kernel agent framework instead of AutoGen.

import asyncio
import os
from typing import Annotated, Literal

import dotenv
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions import kernel_function
from semantic_kernel.kernel import Kernel

from settings import llm_config

dotenv.load_dotenv()

azure_openai_endpoint = os.getenv("AZURE_OPENAI_URL")

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


def setup_chat_service(kernel: Kernel, service_id: str) -> None:
    """Set up a chat completion service for the kernel."""
    deployment_name = llm_config.get("config", {}).get("model", "gpt-4o")
    endpoint = llm_config.get("config", {}).get(
        "azure_endpoint", azure_openai_endpoint
    )
    api_key = llm_config.get("config", {}).get("api_key", None)
    api_version = llm_config.get("config", {}).get("api_version", "2024-06-01")

    chat_service = AzureChatCompletion(
        service_id=service_id,
        endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
        deployment_name=deployment_name,
    )
    kernel.add_service(chat_service)


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
    kernel = Kernel()
    service_id = "math-time-assistant"
    setup_chat_service(kernel, service_id)

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
