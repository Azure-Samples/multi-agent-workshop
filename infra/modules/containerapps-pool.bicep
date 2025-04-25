@description('Tags to apply to resources')
param tags object

@description('Name of the Container Apps environment')
param envName string

@description('Name of the Container Apps managed pool')
param poolName string

@description('Customer ID of the Log Analytics workspace')
param logAnalyticsWorkspaceCustomerId string

@description('Primary shared key of the Log Analytics workspace')
param logAnalyticsWorkspacePrimarySharedKey string

@description('User ID who should be assigned roles')
param userObjectId string

param location string = 'swedencentral'

// Create a Container Apps environment
resource containerAppsEnv 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: envName
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalyticsWorkspaceCustomerId
        sharedKey: logAnalyticsWorkspacePrimarySharedKey
      }
    }
  }
}

// Create a Container Apps managed pool
resource containerAppsManagedPool 'Microsoft.App/sessionPools@2024-02-02-preview' = {
  name: poolName
  location: location
  tags: tags
  properties: {
    environmentId: containerAppsEnv.id
    poolManagementType: 'Dynamic'
    containerType: 'PythonLTS'
    scaleConfiguration: {
      maxConcurrentSessions: 100
    }
    dynamicPoolConfiguration: {
      executionType: 'Timed'
      cooldownPeriodInSeconds: 300
    }
    sessionNetworkConfiguration: {
      status: 'EgressDisabled'
    }
  }
}

// Role assignments for the user
resource contributorRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(containerAppsManagedPool.id, userObjectId, 'Contributor')
  scope: containerAppsManagedPool
  properties: {
    principalId: userObjectId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'b24988ac-6180-42a0-ab88-20f7382dd24c') // Contributor role ID
    principalType: 'User'
  }
}

resource sessionExecutorRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(containerAppsManagedPool.id, userObjectId, 'ContainerApps Session Executor')
  scope: containerAppsManagedPool
  properties: {
    principalId: userObjectId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '0fb8eba5-a2bb-4abe-b1c1-49dfad359bb0') // ContainerApps Session Executor role ID
    principalType: 'User'
  }
}

// Outputs
output environmentId string = containerAppsEnv.id
output managedPoolId string = containerAppsManagedPool.id
output managementEndpoint string = containerAppsManagedPool.properties.poolManagementEndpoint
