# Using Semantic Kernel AgentGroupChat to facilitate communication between agents
# for remote code execution in Azure Container Apps
#
# EXERCISE: Complete the TODO sections to create a working remote code execution system
# This exercise teaches you how to:
# 1. Create agents that can generate and execute code remotely
# 2. Use Azure Container Apps for secure code execution
# 3. Handle authentication and error management
# 4. Implement proper agent communication patterns

import datetime
import os
import re
from typing import Any, Dict, List, Optional

import dotenv
from azure.core.exceptions import ClientAuthenticationError
from azure.identity import DefaultAzureCredential
from semantic_kernel.agents.agent import Agent
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import (
    AzureChatCompletion,
)
from semantic_kernel.exceptions.function_exceptions import (
    FunctionExecutionException,
)
from semantic_kernel.kernel import Kernel

from settings import llm_config

dotenv.load_dotenv()

azure_openai_endpoint = os.getenv("AZURE_OPENAI_URL")
pool_management_endpoint = os.getenv("ACA_POOL_MANAGEMENT_ENDPOINT")


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


def extract_markdown_code_blocks(markdown_text: str) -> List[Dict[str, str]]:
    """Extract code blocks from markdown text."""
    pattern = re.compile(r"```(?:\s*([\w\+\-]+))?\n([\s\S]*?)```")
    matches = pattern.findall(markdown_text)
    code_blocks = []
    for match in matches:
        language = match[0].strip() if match[0] else "python"
        code_content = match[1]
        code_blocks.append({"code": code_content, "language": language})
    return code_blocks


def auth_callback_factory(scope):
    auth_token = None

    async def auth_callback() -> str:
        """Auth callback for the SessionsPythonTool.
        This is a sample auth callback that shows how to use Azure's DefaultAzureCredential
        to get an access token.
        """
        nonlocal auth_token
        current_utc_timestamp = int(
            datetime.datetime.now(datetime.timezone.utc).timestamp()
        )

        if not auth_token or auth_token.expires_on < current_utc_timestamp:
            credential = DefaultAzureCredential()

            try:
                auth_token = credential.get_token(scope)
            except ClientAuthenticationError as cae:
                err_messages = getattr(cae, "messages", [])
                raise FunctionExecutionException(
                    f"Failed to retrieve the client auth token with messages: {' '.join(err_messages)}"
                ) from cae

        return auth_token.token

    return auth_callback


class RemoteCodeExecutor:
    """
    A code executor that runs code blocks in a remote Azure Container Apps instance.
    This allows for secure execution in an isolated environment with appropriate resources.

    Requirements for ACA ingress configuration:
    1. Your ACA container must have ingress enabled with an external endpoint
    2. The endpoint should be HTTPS for production use
    3. IP restrictions should be configured if needed for security
    4. Authentication should be enabled (API key is used in this code)
    """

    def __init__(
        self,
        timeout: Optional[int] = 60,
        pool_management_endpoint: Optional[str] = None,
    ) -> None:
        """
        Initialize the RemoteCodeExecutor with connection details for Azure Container Apps.

        Args:
            timeout: Maximum time in seconds to wait for code execution
            pool_management_endpoint: Endpoint for the Azure Container Apps session pool
            additional_session_config: Additional configuration parameters for the session
        """
        # TODO: Store the timeout parameter
        self.timeout = None  # Replace None with the timeout parameter

        # TODO: Set the pool management endpoint
        # Use the parameter if provided, otherwise get from environment variable
        # Default to a TODO message if not found
        self.pool_management_endpoint = None  # Complete this assignment

    async def execute_code_blocks(
        self, code_blocks: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Execute a list of code blocks in the remote Azure Container Apps instance.

        Args:
            code_blocks: List of dictionaries with 'code' and 'language' keys

        Returns:
            Dictionary with execution output and status
        """
        # Initialize logs list and exit_code variable
        logs = []
        exit_code = 0

        try:
            # TODO: Create a SessionsPythonTool instance
            # Use the pool_management_endpoint and auth_callback_factory
            # Hint: Use the scope "https://dynamicsessions.io/.default"
            sessions_tool = (
                None  # Replace with proper SessionsPythonTool initialization
            )

            # TODO: Execute each code block in sequence
            for i, code_block in enumerate(code_blocks):
                try:
                    # TODO: Create a block header for logging
                    block_header = ""  # Create a header like "--- Executing code block 1/3 ---"
                    logs.append(block_header)

                    # TODO: Execute the code in the remote session
                    # Use sessions_tool.execute_code() with the code_block["code"]
                    # Remember this is an async method
                    result = None  # Replace with actual execution

                    # TODO: Append the result to logs
                    logs.append("")  # Convert result to string and append

                except Exception:
                    # TODO: Handle execution errors
                    # Create an error message including the block number and error
                    error_msg = ""  # Create appropriate error message
                    logs.append(error_msg)

                    # TODO: Set exit code to indicate failure
                    exit_code = 1  # This is correct
                    break

            # TODO: Combine all logs into a single string
            log_output = ""  # Join all logs

            # TODO: Return the result dictionary
            return {}  # Return dict with "exit_code" and "output" keys

        except Exception as e:
            # TODO: Handle authentication or connection errors
            # Check if it's an authentication error and provide appropriate message
            if "authentication" in str(e).lower():
                return {
                    "exit_code": 1,
                    "output": "Authentication error: " + str(e),
                }
            else:
                return {"exit_code": 1, "output": "Execution error: " + str(e)}


async def create_code_executor_agent(
    remote_executor: RemoteCodeExecutor,
) -> Agent:
    """Create an agent specialized in executing Python code remotely."""
    # Create a kernel and set up the chat service
    kernel = Kernel()
    service_id = "remote-code-execution-service"
    # TODO: Call setup_chat_service with kernel and service_id

    # TODO: Create an agent description
    # The agent should describe its role in executing Python code remotely
    description = """TODO: Write a description for the remote code executor agent.
    This agent should:
    - Execute Python code in a remote Azure Container Apps instance
    - Report execution results and errors
    - Handle code blocks in markdown format
    """

    # TODO: Create the ChatCompletionAgent
    # Use name="RemoteExecutor", description=description, kernel=kernel
    code_executor_agent = None  # Create the agent

    # Store the remote executor for later use
    code_executor_agent._remote_executor = remote_executor

    return code_executor_agent


async def create_assistant_agent() -> Agent:
    """Create an assistant agent that generates Python code."""
    # TODO: Create a kernel and set up the chat service
    kernel = None  # Create Kernel instance
    service_id = "assistant-service"
    # TODO: Call setup_chat_service with kernel and service_id

    # TODO: Create an agent description
    # The agent should describe its role in generating Python code
    description = """TODO: Write a description for the assistant agent.
    This agent should:
    - Generate Python code in markdown code blocks
    - Save figures to files (never use plt.show())
    - Provide complete code in a single response
    - Ask the RemoteExecutor to execute the code
    """

    # TODO: Create the ChatCompletionAgent
    # Use name="Assistant", description=description, kernel=kernel
    assistant_agent = None  # Create the agent

    return assistant_agent


async def main():
    """
    Main function to set up and run coding agents with remote execution.
    This function runs code in an Azure Container Apps instance for secure execution.
    """

    remote_executor = RemoteCodeExecutor()

    # TODO: Create the agents
    assistant_agent = None  # Create assistant agent
    executor_agent = None  # Create executor agent with remote_executor

    # TODO: Set up the initial chat history
    chat_history = None  # Create ChatHistory instance

    # TODO: Add a system message to the chat history
    # Describe that the agents work together to generate and execute code

    # TODO: Add the user's request to chat history
    user_request = "Write Python code to calculate the 14th Fibonacci number."
    # Add this as a user message to chat_history

    print(f"User: {user_request}")
    print("\n--- Starting remote coding session ---\n")

    # TODO: Create an agent group chat
    # Use the assistant_agent, executor_agent, and chat_history
    group_chat = None  # Create AgentGroupChat

    # TODO: Set up message tracking variables
    message_count = 0
    max_iterations = 6  # Limit iterations to prevent infinite loops
    code_executed = False  # Track if code has been executed

    # TODO: Process the conversation
    # Use async for loop with group_chat.invoke()
    async for message in None:  # Replace None with proper iterator
        message_count += 1

        # TODO: Get the agent name from the message
        agent_name = "Unknown Agent"  # Extract name from message

        # TODO: Get the message content
        content = ""  # Extract content from message

        # Print the message with agent name
        print(f"\n{'-' * 80}")
        print(f"[{agent_name}]: {content}")

        # TODO: Check if this is from Assistant and contains code blocks
        if (
            agent_name == "Assistant"
            and "```" in content
            and not code_executed
        ):
            # TODO: Extract code blocks from the content
            code_blocks = None  # Use extract_markdown_code_blocks function

            if code_blocks:
                print(f"\n{'-' * 80}")
                print("Executing code remotely...")

                # TODO: Execute the code blocks
                execution_result = (
                    None  # Use remote_executor.execute_code_blocks
                )

                print("Remote Execution Result:")
                print(f"Exit Code: {execution_result['exit_code']}")
                print(f"Output:\n{execution_result['output']}")

                code_executed = True

                # TODO: Check if execution was successful
                if execution_result["exit_code"] == 0:
                    print("\n--- Code executed successfully! ---")
                    break

        # TODO: Break if we've reached max iterations
        if message_count >= max_iterations:
            print(f"\n--- Reached maximum iterations ({max_iterations}) ---")
            break

    print("\n--- Remote coding session completed ---\n")


if __name__ == "__main__":
    # TODO: Run the main function
    # Use asyncio.run() to execute the main function
    pass  # Replace with proper execution
