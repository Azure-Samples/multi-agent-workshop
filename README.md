


# Multi-Agent Workshop

This project showcases autogen (0.4) by presenting a set of simple scripts that create different type of agents and interactions between them with the purpose of highlighting the main capabilities of the agentic framework. This repo is based on [https://github.com/krishsub/MultiagentHackathon](https://github.com/krishsub/MultiagentHackathon).


## Getting Started

### Prerequisites

- dev container option: The project provides a devcontainer configuration that can be used with github codespaces or your own local dev container. So, if you opt for this, you need to have docker in your system
- venv option: if you have python > 3.8 you could choose to create a venv and install all the requirements there. 


### Quickstart

#### Environment Variables
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

Then run the server directly (this will automatically install dependencies):
```bash
uv run 0X_SCRIPT_NAME.py
```

#### Option 2: Using pip
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the WebSocket server:
   ```bash
   python 0X_SCRIPT_NAME.py
   ```