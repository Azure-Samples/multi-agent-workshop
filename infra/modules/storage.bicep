@description('Name of the storage account')
param storageName string
var storageNameCleaned = replace(storageName, '-', '')

@description('Location of the storage account')
param location string

@description('Tags for the storage account')
param tags object

@allowed([
  'Standard_LRS'
  'Standard_ZRS'
  'Standard_GRS'
  'Standard_GZRS'
  'Standard_RAGRS'
  'Standard_RAGZRS'
  'Premium_LRS'
  'Premium_ZRS'
])

@description('Storage SKU')
param storageSkuName string = 'Standard_LRS'

@description('Specifies the object id of a Miccrosoft Entra ID user. In general, this the object id of the system administrator who deploys the Azure resources.')
param userObjectId string

@description('Specifies the principal id of the Azure OpenAI.')
param openAiPrincipalId string

@description('Specifies the minimum TLS version to be used by the storage account.')
@allowed([
  'TLS1_0'
  'TLS1_1'
  'TLS1_2'
])
param minimumTlsVersion string = 'TLS1_2'

@description('Specifies whether to allow public access to the storage account.')
@allowed([
  'Enabled'
  'Disabled'
])
param allowStorageAccountPublicAccess string = 'Enabled'

@description('Specifies whether to allow shared key access to the storage account.')
param allowSharedKeyAccess bool = true

@description('Specifies whether to allow blob public access.')
param allowBlobPublicAccess bool = true

@description('Specifies whether to allow cross-tenant replication of data in the storage account.')
param allowCrossTenantReplication bool = false

@description('Specifies whether to support HTTPS traffic only.')
param supportsHttpsTrafficOnly bool = false

@description('Specifies the access tier for the storage account.')
@allowed([
  'Hot'
  'Cool'
])
param accessTier string = 'Hot'

@description('The default action of allow or deny when no other rules match. Allowed values: Allow or Deny')
@allowed([
  'Allow'
  'Deny'
])
param networkAclsDefaultAction string = 'Allow'

@description('Specifies whether to create containers.')
param createContainers bool = false
@description('Specifies an array of containers to create.')
param containerNames array = []


resource storageAccount 'Microsoft.Storage/storageAccounts@2022-09-01' = {
  name: storageNameCleaned
  location: location
  tags: tags
  sku: {
    name: storageSkuName
  }
  kind: 'StorageV2'

    // Containers live inside of a blob service
    resource blobService 'blobServices' = {
      name: 'default'
  
      // Creating containers with provided names if contition is true
      resource containers 'containers' = [
        for containerName in containerNames: if (createContainers) {
          name: containerName
          properties: {
            publicAccess: 'None'
          }
        }
      ]
    }

  properties: {
    accessTier: accessTier
    allowBlobPublicAccess: allowBlobPublicAccess
    allowCrossTenantReplication: allowCrossTenantReplication
    allowSharedKeyAccess: allowSharedKeyAccess
    encryption: {
      keySource: 'Microsoft.Storage'
      requireInfrastructureEncryption: false
      services: {
        blob: {
          enabled: true
          keyType: 'Account'
        }
        file: {
          enabled: true
          keyType: 'Account'
        }
        queue: {
          enabled: true
          keyType: 'Service'
        }
        table: {
          enabled: true
          keyType: 'Service'
        }
      }
    }
    isHnsEnabled: false
    isNfsV3Enabled: false
    keyPolicy: {
      keyExpirationPeriodInDays: 7
    }
    largeFileSharesState: 'Disabled'
    minimumTlsVersion: minimumTlsVersion
    networkAcls: {
      bypass: 'AzureServices'
      defaultAction: networkAclsDefaultAction
    }
    publicNetworkAccess: allowStorageAccountPublicAccess
    supportsHttpsTrafficOnly: supportsHttpsTrafficOnly
  }
}
resource storageAccountContributorRoleDefinition 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: '17d1049b-9a84-46fb-8f53-869881c3d3ab'
  scope: subscription()
}

resource storageBlobDataContributorRoleDefinition 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
  scope: subscription()
}

resource storageFileDataPrivilegedContributorRoleDefinition 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: '69566ab7-960f-475b-8e7c-b3118f30c6bd'
  scope: subscription()
}

resource storageTableDataContributorRoleDefinition 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: '0a9a7e1f-b9d0-4cc4-a60d-0319b160aaa3'
  scope: subscription()
}

// This role assignment grants the user the required permissions to create a Prompt Flow in Azure AI Foundry
resource storageAccountContributorUserRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(userObjectId)) {
  name: guid(storageAccount.id, storageAccountContributorRoleDefinition.id, userObjectId)
  scope: storageAccount
  properties: {
    roleDefinitionId: storageAccountContributorRoleDefinition.id
    principalType: 'User'
    principalId: userObjectId
  }
}

resource storageBlobDataContributorUserRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(userObjectId)) {
  name: guid(storageAccount.id, storageBlobDataContributorRoleDefinition.id, userObjectId)
  scope: storageAccount
  properties: {
    roleDefinitionId: storageBlobDataContributorRoleDefinition.id
    principalType: 'User'
    principalId: userObjectId
  }
}

resource storageFileDataPrivilegedContributorUserRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(userObjectId)) {
  name: guid(storageAccount.id, storageFileDataPrivilegedContributorRoleDefinition.id, userObjectId)
  scope: storageAccount
  properties: {
    roleDefinitionId: storageFileDataPrivilegedContributorRoleDefinition.id
    principalType: 'User'
    principalId: userObjectId
  }
}

resource storageTableDataContributorUserRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(userObjectId)) {
  name: guid(storageAccount.id, storageTableDataContributorRoleDefinition.id, userObjectId)
  scope: storageAccount
  properties: {
    roleDefinitionId: storageTableDataContributorRoleDefinition.id
    principalType: 'User'
    principalId: userObjectId
  }
}

// This role assignment grants the Azure AI Services managed identity the required permissions to access and transcribe the input audio and video files stored in the storage account
resource storageBlobDataContributorManagedIdentityRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(openAiPrincipalId)) {
  name: guid(storageAccount.id, storageBlobDataContributorRoleDefinition.id, openAiPrincipalId)
  scope: storageAccount
  properties: {
    roleDefinitionId: storageBlobDataContributorRoleDefinition.id
    principalType: 'ServicePrincipal'
    principalId: openAiPrincipalId
  }
}

output id string = storageAccount.id
output name string = storageAccount.name
