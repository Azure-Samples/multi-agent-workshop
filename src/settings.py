import os

from dotenv import load_dotenv
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.kernel import Kernel

load_dotenv()


llm_config = {
    "provider": "AzureOpenAIChatCompletionClient",
    "config": {
        "model": "gpt-4o",
        "api_key": os.environ.get("AZURE_OPENAI_API_KEY", ""),
        "azure_endpoint": os.environ.get("AZURE_OPENAI_URL", ""),
        "api_version": "2024-06-01",
    },
}


def setup_kernel_with_chat_completion_service(service_id: str) -> Kernel:
    """Set up a chat completion service and the kernel."""
    kernel = Kernel()
    deployment_name = os.environ.get(
        "AZURE_OPENAI_MODEL_DEPLOYMENT_NAME", "gpt-4o"
    )
    endpoint = os.environ.get("AZURE_OPENAI_URL", "")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY", "")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-06-01")

    chat_service = AzureChatCompletion(
        service_id=service_id,
        endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
        deployment_name=deployment_name,
    )
    kernel.add_service(chat_service)
    return kernel


# llm_websurfer = {
#     "temperature": 0,
#     "cache_seed": None,
#     "config_list": [
#         {
#             "model": "gpt-4o",
#             "api_type": "azure",
#             "api_key": os.environ.get("AZURE_OPENAI_API_KEY", ""),
#             "base_url": os.environ.get("AZURE_OPENAI_URL", ""),
#             "api_version": "2024-08-01-preview",
#         }
#     ],
# }

# browser_config = {
#     "viewport_size": 4096,
#     "bing_api_key": os.environ.get(bing_api_key_name),
# }

generated_directory = "./generated"

# if os.environ.get(bing_api_key_name) is None:
#     print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#     print("WARNING: Bing API key not found. Some examples won't work.")
#     print(f"Set the environment variable {bing_api_key_name}")
#     print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

if os.environ.get("AZURE_OPENAI_API_KEY") is None:
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(
        "WARNING: Azure OpenAI API key not found. None of the examples will work."
    )
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

if os.environ.get("AZURE_OPENAI_URL") is None:
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(
        "WARNING: Azure OpenAI API URL not found. None of the examples will work."
    )
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
