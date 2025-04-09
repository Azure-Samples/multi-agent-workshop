@description('Container registry name')
param containerRegistryName string
var containerRegistryNameCleaned = replace(containerRegistryName, '-', '')

@description('Container registry location')
param location string

@description('Container registry tags')
param tags object


resource containerRegistry 'Microsoft.ContainerRegistry/registries@2021-09-01' = {
  name: containerRegistryNameCleaned
  location: location
  tags: tags
  sku: {
    name: 'Premium'
  }
  properties: {
    adminUserEnabled: true
    dataEndpointEnabled: false
    networkRuleBypassOptions: 'AzureServices'
    networkRuleSet: {
      defaultAction: 'Allow'
    }
    policies: {
      retentionPolicy: {
        status: 'enabled'
        days: 7
      }
    }
    publicNetworkAccess: 'Enabled'
    zoneRedundancy: 'Disabled'
  }
}

output containerRegistryId string = containerRegistry.id
