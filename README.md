
# Multi-Agent Workshop

This project showcases autogen (0.4) by presenting a set of simple scripts that create different type of agents and interactions between them with the purpose of highlighting the main capabilities of the agentic framework. This repo is based on [https://github.com/krishsub/MultiagentHackathon](https://github.com/krishsub/MultiagentHackathon).

## Getting Started

### Prerequisites

- Open AI service deployed with GPT-4o
- Azure Container Apps Session Pool

### Development environment

- Dev container option: The project provides a devcontainer configuration that can be used with github codespaces or your own local dev container. So, if you opt for this, you need to have docker on your system.
- Virtual Environment option: if you have python > 3.8 you could choose to create a venv and install all the requirements there.

#### Leverage AZD to deploy the prerequisites

You can leverage the [Azure Developer CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/), `azd` for short, to deploy the prerequisites to a subscription. It'll create the resources and export some environment variables which you can use to run the exercises. To leverage `azd` you need to have it installed and configured. After that, all it takes is a simple `azd up` and the components will be installed.

For a detailed explanation on what it deploys, check out the [README.md in the infra directory](/infra/README.md).

After the components have been deployed, you can navigate to [AI Foundry](https://ai.azure.com/) and obtain the Open AI Key and Endpoint. The Open AI endpoint, as well as the Azure Container Apps endpoint, will be stored in the `azd` environment variables. You can leverage those as well. The Open AI Key is not exposed in this manner for security considerations.

### Quickstart

#### Environment Variables

For this set of scripts, a gpt-4o model instance was used.
Create a `.env` file with your Azure OpenAI credentials in the `src` folder:

```bash
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=your_endpoint
```

#### Installation

Choose one of the following methods to run the different scripts. Make sure to `cd src`.

#### Option 1: Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and runner. If you haven't installed it yet:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then run the script directly (this will automatically install dependencies):

```bash
uv run 0X_SCRIPT_NAME.py
```

#### Option 2: Using pip

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the script:

   ```bash
   python 0X_SCRIPT_NAME.py
   ```
