# Copyright (c) Microsoft. All rights reserved.
"""
GitHub Issue Query Agent Exercise

This exercise demonstrates how to create a chat completion agent that
answers questions about Github using a Semantic Kernel Plugin from a MCP server.

Requirements:
- Azure OpenAI API credentials in environment variables
- GitHub Personal Access Token in environment variables
- Docker installed and running

Learning objectives:
- Working with Semantic Kernel agents
- Integrating MCP plugins with Docker
- Managing conversation threads
- Using GitHub APIs through MCP
"""

import asyncio
import os

import dotenv
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.mcp import MCPStdioPlugin
from semantic_kernel.kernel import Kernel

from settings import llm_config

dotenv.load_dotenv()

azure_openai_endpoint = os.getenv("AZURE_OPENAI_URL")

# Test conversation inputs - feel free to modify these
USER_INPUTS = [
    "What are the latest 5 python issues in Microsoft/semantic-kernel?",
    "Are there any untriaged python issues?",
    "What is the status of issue #10785?",
]


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
    - Define an appropriate service_id
    - Call setup_chat_service with your kernel and service_id
    """
    kernel = None  # Your code here
    service_id = None  # Your code here
    # Your setup code here

    """
    TODO 2: Set up the GitHub MCP Plugin
    - Create an MCPStdioPlugin for GitHub interaction
    - Configure the plugin with:
        - Appropriate name and description
        - Docker command and arguments
        - GitHub token from environment variables
    - Handle the plugin in an async context manager
    
    Hint: The plugin should use ghcr.io/github/github-mcp-server Docker image
    """
    async with MCPStdioPlugin(
        name=None,  # Add appropriate name
        description=None,  # Add appropriate description
        command="docker",
        args=[
            # Add appropriate Docker arguments here
            # Remember to include GitHub token configuration
        ],
        env={
            # Add necessary environment variables
        },
    ) as github_plugin:
        """
        TODO 3: Create the Chat Completion Agent
        - Initialize a ChatCompletionAgent with:
            - The configured kernel
            - Appropriate name and instructions
            - The GitHub plugin
        """
        agent = None  # Your agent initialization code here

        """
        TODO 4: Implement the Conversation Loop
        - For each input in USER_INPUTS:
            - Initialize or reset the conversation thread
            - Send the user input to the agent
            - Print the response
            - Store the thread for context
        """
        for user_input in USER_INPUTS:
            # Your conversation handling code here
            pass

        """
        TODO 5: Clean Up Resources
        - Implement proper thread cleanup
        - Ensure all resources are properly released
        """
        # Your cleanup code here


"""
Expected Output Example:

# User: What are the latest 5 python issues in Microsoft/semantic-kernel?
# IssueAgent: [Formatted list of issues with details]

# User: Are there any untriaged python issues?
# IssueAgent: [Yes/No response with details]

# User: What is the status of issue #10785?
# IssueAgent: [Status details of the specific issue]
"""

if __name__ == "__main__":
    asyncio.run(main())
