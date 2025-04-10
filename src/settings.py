import os

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

load_dotenv()

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

if os.environ.get("AZURE_OPENAI_URL") is None:
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("WARNING: Azure OpenAI API URL not found. None of the examples will work.")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
