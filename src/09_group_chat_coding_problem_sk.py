# Using AgentGroupChat to facilitate communication between agents

import asyncio
import datetime
import os

import dotenv
from azure.core.exceptions import ClientAuthenticationError
from semantic_kernel.agents import ChatCompletionAgent, AgentGroupChat
from semantic_kernel.agents.agent import Agent
from semantic_kernel.agents.group_chat.agent_group_chat import AgentGroupChat
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import (
    AzureChatCompletion,
)
from semantic_kernel.contents import (
    AuthorRole,
    ChatHistory,
    ChatMessageContent,
)
from semantic_kernel.core_plugins.sessions_python_tool.sessions_python_plugin import (
    SessionsPythonTool,
)
from semantic_kernel.exceptions.function_exceptions import (
    FunctionExecutionException,
)
from semantic_kernel.kernel import Kernel
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

dotenv.load_dotenv()

azure_openai_endpoint = os.getenv("AZURE_OPENAI_URL")
pool_management_endpoint = os.getenv("ACA_POOL_MANAGEMENT_ENDPOINT")


def auth_callback_factory(scope):
    auth_token = None

    async def auth_callback() -> str:
        """Auth callback for the SessionsPythonTool."""
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


def setup_chat_service(kernel: Kernel, service_id: str) -> None:
    """Set up a chat completion service for the kernel."""
    deployment_name = "gpt-4o"
    endpoint = os.environ.get("AZURE_OPENAI_URL", "")
    api_version = "2024-06-01"
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

    chat_service = AzureChatCompletion(
        service_id=service_id,
        endpoint=endpoint,
        api_version=api_version,
        deployment_name=deployment_name,
        ad_token_provider=token_provider,
    )
    kernel.add_service(chat_service)


async def create_code_agent() -> Agent:
    """Create an agent specialized in executing Python code."""
    kernel = Kernel()
    service_id = "code-execution-service"
    setup_chat_service(kernel, service_id)

    # Set up Python code interpreter
    python_code_interpreter = SessionsPythonTool(
        service_url=pool_management_endpoint,
        auth_callback=auth_callback_factory(
            "https://dynamicsessions.io/.default"
        ),
    )
    # Add the Python code interpreter plugin directly to the kernel
    plugin = kernel.add_plugin(
        python_code_interpreter, "PythonCodeInterpreter"
    )

    # Create agent description - mention the plugin's availability
    description = """I am a Python Code Execution Agent. 
    I can run Python code to solve problems using the PythonCodeInterpreter plugin.
    I can execute code with the execute_code function.
    I always include in my answer if I used the PythonCodeInterpreter plugin.
    """
    #     DO NOT provide explanations unless asked - just execute the code and return the result.

    # Create the agent using ChatCompletionAgent with minimal parameters
    # The kernel already contains the plugin, so the agent can use it
    code_agent = ChatCompletionAgent(
        name="CodeAgent",
        description=description,
        kernel=kernel,
    )

    return code_agent


async def create_chat_agent() -> Agent:
    """Create a chat agent that interacts with users."""
    kernel = Kernel()
    service_id = "chat-service"
    setup_chat_service(kernel, service_id)

    # Create agent description
    description = """I am a Math Problem Solver. 
    I help solve math problems by creating Python code and asking CodeAgent to execute it.
    When asked to solve a math problem:
    1. Create Python code that solves the problem
    2. Ask CodeAgent to execute the code: "@CodeAgent please execute this code: ```python\\n<code>\\n```"
    3. Wait for the result and provide a final answer
    4. I always confirm with the @CodeAgent if he executed the code to solve the problem, because I don't trust results
    without verification.
    """

    # Create the agent using ChatCompletionAgent with minimal parameters
    chat_agent = ChatCompletionAgent(
        name="MathAgent",
        description=description,
        kernel=kernel,
        # Remove any service_id parameter - the kernel already has the service
    )

    return chat_agent


async def main():
    # Create the agents
    code_agent = await create_code_agent()
    chat_agent = await create_chat_agent()

    # Create an agent group chat with the correct parameters
    group_chat = AgentGroupChat(agents=[chat_agent, code_agent])

    # Set up the initial chat history
    chat_history = ChatHistory()
    chat_history.add_system_message(
        "You are a team working together to solve math problems. "
        "The user will ask a question, and you'll collaborate to solve it."
    )

    # Add the user's question
    user_question = "Calculate the fibonacci number of 10"
    chat_history.add_user_message(user_question)

    print(f"User: {user_question}")
    print("\n--- Starting group chat ---\n")

    await group_chat.add_chat_message(
        ChatMessageContent(role=AuthorRole.USER, content=user_question)
    )

    # Improved message handling - display who's speaking
    async for message in group_chat.invoke():
        # Access the name attribute directly
        agent_name = (
            message.name if hasattr(message, "name") else "Unknown Agent"
        )

        # Get the message content
        content = ""
        if hasattr(message, "content"):
            content = message.content
        elif hasattr(message, "items") and message.items:
            for item in message.items:
                if hasattr(item, "text") and item.text:
                    content += item.text

        # Print the message with agent name
        print(f"\n[{agent_name}]: {content}")

        # Print additional debug info if needed
        if not content:
            print(f"Message details: {message}")

    print("\n--- Group chat completed ---\n")


if __name__ == "__main__":
    asyncio.run(main())
