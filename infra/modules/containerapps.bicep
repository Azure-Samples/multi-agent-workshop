
@description('Tags to apply to resources')
param tags object

@description('Name of the Container Apps environment')
param envName string

@description('Name of the Container Apps managed pool')
param poolName string

// Create a Log Analytics workspace for the Container Apps environment
resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: '${envName}-logs'
  location: 'swedencentral'
  tags: tags
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
    features: {
      enableLogAccessUsingOnlyResourcePermissions: true
    }
  }
}

// Create a Container Apps environment
resource containerAppsEnv 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: envName
  location: 'swedencentral'
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalyticsWorkspace.properties.customerId
        sharedKey: logAnalyticsWorkspace.listKeys().primarySharedKey
      }
    }
  }
}

// Create a Container Apps managed pool
resource containerAppsManagedPool 'Microsoft.App/sessionPools@2024-02-02-preview' = {
  name: poolName
  location: 'swedencentral'
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

// Outputs
output environmentId string = containerAppsEnv.id
output managedPoolId string = containerAppsManagedPool.id
output managementEndpoint string = containerAppsManagedPool.properties.poolManagementEndpoint
