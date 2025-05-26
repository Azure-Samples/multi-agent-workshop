# Copyright (c) Microsoft. All rights reserved.
"""
Restaurant Booking Agent with MCP Integration - Exercise

This is an exercise file where you'll implement a restaurant booking system
using Semantic Kernel and MCP (Model Context Protocol) plugins.

The system should:
- Handle restaurant menu queries
- Process restaurant bookings
- Maintain conversation context
- Use MCP plugins for specialized functionality

Requirements:
- Azure OpenAI API credentials in environment variables
- Semantic Kernel with MCP support installed
- MCP plugin servers in the 'servers_mcp' directory
"""

import asyncio
import os

import dotenv
from semantic_kernel.agents import ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.mcp import MCPStdioPlugin
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
    """
    TODO 1: Initialize the Kernel and Chat Service
    - Create a new Kernel instance
    - Set up a service_id for the restaurant agent
    - Call setup_chat_service with the kernel and service_id
    """
    kernel = None  # Your code here
    service_id = None  # Your code here
    # Your code here

    """
    TODO 2: Set up the Menu Plugin
    - Create an MCPStdioPlugin for the menu service
    - Configure the plugin with:
        - Appropriate name and description
        - Command to run the menu server
        - Correct directory path for the server
    Hint: Use Path to handle file paths correctly
    """

    """
    TODO 3: Set up the Booking Plugin
    - Create an MCPStdioPlugin for the booking service
    - Configure similar to the menu plugin but for booking functionality
    - Ensure proper path to the booking server
    - The servers are located in the 'src/servers_mcp' directory and contain already the complete code
    """

    async with (
        # Your menu plugin code here
        MCPStdioPlugin(
            name="Menu",
            description="Your description here",
            command="uv",
            args=[
                # Your args here
            ],
        ) as restaurant_agent,
        # Your booking plugin code here
        MCPStdioPlugin(
            name="Booking",
            description="Your description here",
            command="uv",
            args=[
                # Your args here
            ],
        ) as booking_agent,
    ):
        """
        TODO 4: Create the Chat Completion Agent
        - Initialize the agent with the kernel
        - Set appropriate name and instructions
        - Add all necessary plugins (menu, booking, and time)
        """
        agent = None  # Your code here

        """
        TODO 5: Implement the Conversation Loop
        - Initialize the conversation thread
        - Create a loop to handle user input
        - Process 'exit' command
        - Get and display agent responses
        - Maintain conversation thread
        """
        thread: ChatHistoryAgentThread | None = None
        # Your conversation loop code here

        """
        TODO 6: Implement Cleanup
        - Ensure proper cleanup of the conversation thread
        - Handle any necessary resource cleanup
        """
        # Your cleanup code here


"""
Expected conversation flow:

User: what restaurants can I choose from?
Agent: [List of available restaurants]

User: what are the specials at The Farm?
Agent: [List of specials]

User: book a table for 2 people
Agent: [Booking confirmation or alternative suggestions]
"""

if __name__ == "__main__":
    asyncio.run(main())
