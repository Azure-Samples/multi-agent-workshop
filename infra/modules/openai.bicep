@description('Tags to apply to resources')
param tags object

@description('Name of the Azure OpenAI service')
param openAiName string

@description('Specifies the object id of a Miccrosoft Entra ID user. In general, this the object id of the system administrator who deploys the Azure resources.')
param userObjectId string

resource openAi 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: openAiName
  location: 'swedencentral'
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  kind: 'AIServices'
  sku: {
    name: 'S0'
  }
  properties: {
    customSubDomainName: openAiName
    publicNetworkAccess: 'Enabled'
  }
}

// Define the model deployment with hardcoded GPT-4o configuration
resource gpt4oDeployment 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = {
  parent: openAi
  name: 'gpt-4o'
  sku: {
    name: 'Standard'
    capacity: 10
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: 'gpt-4o'
      version: '2024-11-20'
    }
  }
}

resource cognitiveServicesContributorRoleDefinition 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: '25fbc0a9-bd7c-42a3-aa1a-3b75d497ee68'
  scope: subscription()
}

// This role assignment grants the user the required permissions to eventually delete and purge the Azure AI Services account
// https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/role-based-access-control#cognitive-services-contributor
resource cognitiveServicesContributorRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(userObjectId)) {
  name: guid(openAi.id, cognitiveServicesContributorRoleDefinition.id, userObjectId)
  scope: openAi
  properties: {
    roleDefinitionId: cognitiveServicesContributorRoleDefinition.id
    principalType: 'User'
    principalId: userObjectId
  }
}

resource cognitiveServicesOpenAIContributorRoleDefinition 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: 'a001fd3d-188f-4b5d-821b-7da978bf7442'
  scope: subscription()
}

// This role assignment grants the user the required permissions to make inference API calls with Microsoft Entra ID
// https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/role-based-access-control#cognitive-services-openai-contributor
resource cognitiveServicesOpenAIContributorRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(userObjectId)) {
  name: guid(openAi.id, cognitiveServicesOpenAIContributorRoleDefinition.id, userObjectId)
  scope: openAi
  properties: {
    roleDefinitionId: cognitiveServicesOpenAIContributorRoleDefinition.id
    principalType: 'User'
    principalId: userObjectId
  }
}

output id string = openAi.id
output name string = openAi.name
output endpoint string = openAi.properties.endpoint
output openAiEndpoints string = openAi.properties.endpoints['OpenAI Language Model Instance API']
output principalId string = openAi.identity.principalId
