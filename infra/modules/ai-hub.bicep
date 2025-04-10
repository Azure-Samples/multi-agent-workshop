@description('Azure region of the deployment')
param location string

@description('Tags to add to the resources')
param tags object

@description('Specifies the object id of a Miccrosoft Entra ID user. In general, this the object id of the system administrator who deploys the Azure resources.')
param userObjectId string

@description('AI hub name')
param aiHubName string

@description('AI hub display name')
param aiHubFriendlyName string = aiHubName

@description('AI hub description')
param aiHubDescription string

@description('Resource ID of the application insights resource for storing diagnostics logs')
param applicationInsightsId string

@description('Resource ID of the key vault resource for storing connection strings')
param keyVaultId string

@description('Resource ID of the storage account resource for storing experimentation outputs')
param storageAccountId string

@description('Resource ID of the AI Services resource')
param aiServicesId string

@description('Resource ID of the AI Services endpoint')
param aiServicesEndpoint string

resource aiHub 'Microsoft.MachineLearningServices/workspaces@2025-01-01-preview' = {
  name: aiHubName
  location: location
  tags: tags
  kind: 'hub'
  sku: {
    name: 'Standard'
    tier: 'Standard'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    // organization
    friendlyName: aiHubFriendlyName
    description: aiHubDescription

    // dependent resources
    keyVault: keyVaultId
    storageAccount: storageAccountId
    applicationInsights: applicationInsightsId
  }

  resource aiServicesConnection 'connections@2024-01-01-preview' = {
    name: '${aiHubName}-connection'
    properties: {
      category: 'AIServices'
      target: aiServicesEndpoint
      authType: 'AAD'
      isSharedToAll: true
      metadata: {
        ApiType: 'Azure'
        ResourceId: aiServicesId
      }
    }
  }
}

resource azureMLDataScientistRole 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: 'f6c7c914-8db3-469d-8ca1-694a8f32e121'
  scope: subscription()
}

// This role assignment grants the user the required permissions to start a Prompt Flow in a compute service within Azure AI Foundry
resource azureMLDataScientistUserRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(userObjectId)) {
  name: guid(aiHub.id, azureMLDataScientistRole.id, userObjectId)
  scope: aiHub
  properties: {
    roleDefinitionId: azureMLDataScientistRole.id
    principalType: 'User'
    principalId: userObjectId
  }
}

output id string = aiHub.id
output name string = aiHub.name
