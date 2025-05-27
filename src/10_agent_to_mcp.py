# Copyright (c) Microsoft. All rights reserved.
# Modified from original code: https://github.com/microsoft/semantic-kernel/blob/main/python/samples/concepts/mcp/agent_with_mcp_agent.py
""" "
Restaurant Booking Agent with MCP Integration

This script demonstrates how to create and interact with a conversational AI agent
that helps users find restaurants, check menus, and make reservations. The agent
leverages Model Context Protocol (MCP) plugins to provide specialized functionality.

The script sets up a Semantic Kernel-based agent with two MCP-based plugins:
1. Menu Plugin - Provides information about restaurant menus and specials
2. Booking Plugin - Handles restaurant reservation requests

Features:
- Interactive conversation loop with natural language processing
- Integration with Azure OpenAI services for language understanding
- Plugin-based architecture for modular functionality
- Thread-based conversation management for context preservation

Usage:
- Run the script and interact through the command line
- Ask about available restaurants, menu items, prices, or make bookings
- Type 'exit' to end the conversation

Requirements:
- Azure OpenAI API credentials in environment variables
- Proper configuration in settings.llm_config
- MCP plugin servers in the 'servers_mcp' directory

Example conversation flow:
1. User asks about available restaurants
2. User inquires about menu specials
3. User requests pricing information
4. User makes a reservation request
5. Agent confirms booking details

The script demonstrates modern agent architecture with plugin integration,
providing a practical example of building conversational AI applications.
"""

import asyncio
import os
from pathlib import Path

import dotenv
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.mcp import MCPStdioPlugin
from semantic_kernel.core_plugins.time_plugin import TimePlugin
from semantic_kernel.kernel import Kernel

from settings import llm_config

dotenv.load_dotenv()

azure_openai_endpoint = os.getenv("AZURE_OPENAI_URL")


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
    # 1. Create the agent
    kernel = Kernel()
    service_id = "restaurant-agent"
    setup_chat_service(kernel, service_id)

    async with (
        MCPStdioPlugin(
            name="Menu",
            description="Menu plugin, for details about the menu, call this plugin.",
            command="uv",
            args=[
                f"--directory={str(Path(os.path.dirname(__file__)).joinpath('servers_mcp'))}",
                "run",
                "menu_agent_server.py",
            ],
        ) as restaurant_agent,
        MCPStdioPlugin(
            name="Booking",
            description="Restaurant Booking Plugin",
            command="uv",
            args=[
                f"--directory={str(Path(os.path.dirname(__file__)).joinpath('servers_mcp'))}",
                "run",
                "restaurant_agent_booking_server.py",
            ],
        ) as booking_agent,
    ):
        agent = ChatCompletionAgent(
            kernel=kernel,
            name="PersonalAssistant",
            instructions="Help the user with menu checks bookings.",
            plugins=[restaurant_agent, booking_agent, TimePlugin()],
        )

        # 2. Create a thread to hold the conversation
        # If no thread is provided, a new thread will be
        # created and returned with the initial response
        thread: ChatHistoryAgentThread | None = None
        while True:
            user_input = input("User: ")
            if user_input.lower() == "exit":
                break
            # 3. Invoke the agent for a response
            response = await agent.get_response(
                messages=user_input, thread=thread
            )
            print(f"# {response.name}: {response} ")
            thread = response.thread

        # 4. Cleanup: Clear the thread
        await thread.delete() if thread else None


"""
    Example conversation flow:

    User: what restaurants can I choose from?
    # PersonalAssistant: Here are the available restaurants you can choose from:

    1. **The Farm**: A classic steakhouse with a rustic atmosphere.
    2. **The Harbor**: A seafood restaurant with a view of the ocean.
    3. **The Joint**: A casual eatery with a diverse menu.

    Let me know if you would like to make a booking or need more information about any specific restaurant! 
    User: the farm sounds nice, what are the specials there?
    # PersonalAssistant: The specials at The Farm are:

    - **Special Entree:** T-bone steak
    - **Special Salad:** Caesar Salad
    - **Special Drink:** Old Fashioned

    Let me know if you'd like to make a booking or if you need any more information! 
    User: That entree sounds great, how much does it cost?
    # PersonalAssistant: The cost of the T-bone steak at The Farm is $9.99. Would you like to proceed with a booking? 
    User: yes, for 2 people tomorrow
    # PersonalAssistant: I can confirm a booking for 2 people at The Farm for tomorrow, April 17, 2025. What time would you 
    like the reservation? 
    User: at 2000
    # PersonalAssistant: I apologize, but the booking at The Farm for tomorrow at 20:00 has been denied. However, 
    I was able to confirm bookings at the following restaurants:

    - **The Harbor**: Booking confirmed.
    - **The Joint**: Booking confirmed.

    If you'd like to book at one of these restaurants or try a different time or restaurant, just let me know! 
    User: try 21.00
    # PersonalAssistant: Your table for 2 people at The Farm has been successfully booked for tomorrow, April 17, 2025, 
    at 21:00. Enjoy your meal! If you need anything else, feel free to ask. 
    User: exit
"""

if __name__ == "__main__":
    asyncio.run(main())
