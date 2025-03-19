targetScope = 'subscription'

@description('Environment name')
param environmentName string

var uniqueSuffix = substring(uniqueString(subscription().id, environmentName), 0, 5)
var tags = {
  application: 'Multi-Agent Workshop'
  environment: environmentName
}

// Resource naming with suffix
var resourceGroupName = 'rg-${environmentName}-${uniqueSuffix}'
var openAIName = 'openai-${environmentName}-${uniqueSuffix}'
var containerAppsEnvName = 'aca-env-${environmentName}-${uniqueSuffix}'
var managedPoolName = 'aca-pool-${environmentName}-${uniqueSuffix}'

// Create the resource group
resource rg 'Microsoft.Resources/resourceGroups@2023-07-01' = {
  name: resourceGroupName
  location: 'swedencentral'
  tags: tags
}

// Deploy the Azure OpenAI service
module openai 'modules/openai.bicep' = {
  scope: rg
  name: 'openaiDeploy'
  params: {
    tags: tags
    openAiName: openAIName
  }
}

// Deploy Azure Container Apps environment and managed pool
module containerApps 'modules/containerapps.bicep' = {
  scope: rg
  name: 'containerAppsDeploy'
  params: {
    tags: tags
    envName: containerAppsEnvName
    poolName: managedPoolName
  }
}

// Outputs
output AZURE_RESOURCE_GROUP_NAME string = rg.name
output AZURE_OPENAI_ENDPOINT string = openai.outputs.openAIEndpoint
output AZURE_CONTAINER_APPS_MANAGED_POOL_ENDPOINT string = containerApps.outputs.managementEndpoint
