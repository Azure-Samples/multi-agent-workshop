
@description('Specifies the name')
param name string

@description('Specifies the location.')
param location string

@description('Specifies the resource tags.')
param tags object


// Create a Log Analytics workspace for the Container Apps environment
resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: name
  location: location
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

output workspaceId string = logAnalyticsWorkspace.id
output workspaceCustomerId string = logAnalyticsWorkspace.properties.customerId
output workspacePrimarySharedKey string = logAnalyticsWorkspace.listKeys().primarySharedKey
