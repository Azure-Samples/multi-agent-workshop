targetScope = 'subscription'

@description('Environment name')
param environmentName string

@description('User ID who should be the owner of the resources')
param userObjectId string

var uniqueSuffix = substring(uniqueString(subscription().id, environmentName), 0, 5)
var tags = {
  application: 'Multi-Agent Workshop'
  environment: environmentName
}

// Resource naming with suffix
var resourceGroupName = 'rg-${environmentName}-${uniqueSuffix}'
var openAIName = 'openai-${environmentName}-${uniqueSuffix}'
var aiHubName = 'ai-hub-${environmentName}-${uniqueSuffix}'
var aiProjectName = 'ai-project-${environmentName}-${uniqueSuffix}'
var containerAppsEnvName = 'aca-env-${environmentName}-${uniqueSuffix}'
var managedPoolName = 'aca-pool-${environmentName}-${uniqueSuffix}'

// Create the resource group
resource rg 'Microsoft.Resources/resourceGroups@2023-07-01' = {
  name: resourceGroupName
  location: 'swedencentral'
  tags: tags
}

module logAnalytics 'modules/log-analytics.bicep' = {
  scope: rg
  name: 'logAnalyticsDeploy'
  params: {
    tags: tags
    name: '${rg.name}-la'
    location: rg.location
  }
}

// Deploy the Azure OpenAI service
module openai 'modules/openai.bicep' = {
  scope: rg
  name: 'openaiDeploy'
  params: {
    tags: tags
    openAiName: openAIName
    userObjectId: userObjectId
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
    logAnalyticsWorkspaceCustomerId: logAnalytics.outputs.workspaceCustomerId
    logAnalyticsWorkspacePrimarySharedKey: logAnalytics.outputs.workspacePrimarySharedKey
  }
}

module appInsights 'modules/app-insights.bicep' = {
  scope: rg
  name: 'appInsightsDeploy'
  params: {
    tags: tags
    applicationInsightsName: '${rg.name}-ai'
    location: rg.location
  }
}

module keyvault 'modules/keyvault.bicep' = {
  scope: rg
  name: 'keyvaultDeploy'
  params: {
    tags: tags
    keyvaultName: '${rg.name}-kv'
    location: rg.location
    userObjectId: userObjectId
    workspaceId: logAnalytics.outputs.workspaceId
  }
}

module containerRegistry 'modules/container-registry.bicep' = {
  scope: rg
  name: 'containerRegistryDeploy'
  params: {
    tags: tags
    containerRegistryName: '${rg.name}acr'
    location: rg.location
  }
}

module storageAccount 'modules/storage.bicep' = {
  scope: rg
  name: 'storageAccountDeploy'
  params: {
    tags: tags
    storageName: '${rg.name}sa'
    location: rg.location
    userObjectId: userObjectId
    openAiPrincipalId: openai.outputs.principalId
  }
}

module aiHub 'modules/ai-hub.bicep' = {
  scope: rg
  name: 'aiHubDeploy'
  params: {
    tags: tags
    location: rg.location
    aiHubName: aiHubName
    aiHubFriendlyName: 'AI Hub ${environmentName}'
    aiHubDescription: 'AI Hub for ${environmentName}'
    keyVaultId: keyvault.outputs.keyVaultId
    storageAccountId: storageAccount.outputs.id
    applicationInsightsId: appInsights.outputs.applicationInsightsID
    containerRegistryId: containerRegistry.outputs.containerRegistryId
    aiServicesEndpoint: openai.outputs.endpoint
    aiServicesId: openai.outputs.id 
    userObjectId: userObjectId
  }
}

module aiProject 'modules/ai-project.bicep' = {
  scope: rg
  name: 'aiProjectDeploy'
  params: {
    tags: tags
    location: rg.location
    name: aiProjectName
    friendlyName: 'AI Project for ${environmentName}'
    hubId: aiHub.outputs.id
    workspaceId: logAnalytics.outputs.workspaceId
    userObjectId: userObjectId
    aiServicesPrincipalId: openai.outputs.principalId
  }
}

// Outputs
output AZURE_RESOURCE_GROUP_NAME string = rg.name
output AZURE_OPENAI_ENDPOINT string = openai.outputs.openAiEndpoints
output AZURE_CONTAINER_APPS_MANAGED_POOL_ENDPOINT string = containerApps.outputs.managementEndpoint
