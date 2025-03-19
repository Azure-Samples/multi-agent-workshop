# Infrastructure Setup

This directory contains the Azure infrastructure deployment files using Bicep. The infrastructure setup includes Azure OpenAI services and Azure Container Apps environment required for running the multi-agent workshop.

## File Structure

- `main.bicep` - The main deployment file that orchestrates the creation of all resources
  - Creates a resource group
  - Deploys Azure OpenAI service
  - Sets up Azure Container Apps environment with a managed pool
  - Handles resource naming with unique suffixes

- `modules/openai.bicep` - Module for Azure OpenAI service deployment
  - Deploys an Azure OpenAI service instance
  - Configures GPT-4 model deployment
  - Enables public network access
  - Located in Sweden Central region

- `modules/containerapps.bicep` - Module for Container Apps environment setup
  - Creates a Log Analytics workspace for monitoring
  - Sets up a Container Apps environment
  - Deploys a managed pool for Python containers
  - Configures dynamic scaling and network settings

## Resource Naming

Resources are named using a consistent pattern that includes:
- Environment name (provided as a parameter)
- A unique suffix derived from the subscription ID
- Appropriate prefixes for each resource type (e.g., 'openai-', 'aca-env-')

## Tags

All resources are tagged with:
- application: 'Multi-Agent Workshop'
- environment: [YOUR ENVIRONMENT NAME HERE]

## Outputs

The deployment provides several important outputs including:
- Resource group name as AZURE_RESOURCE_GROUP_NAME
- OpenAI endpoint as AZURE_OPENAI_ENDPOINT
- Container Apps managed pool management endpoint as AZURE_CONTAINER_APPS_MANAGED_POOL_ENDPOINT

These outputs can be used by other parts of the system to interact with the deployed resources.