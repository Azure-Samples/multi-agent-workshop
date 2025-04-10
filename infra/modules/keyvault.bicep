@description('The name of the Key Vault')
param keyvaultName string

@description('The location of the Key Vault')
param location string

@description('The tags for the Key Vault')
param tags object

@description('Specifies the resource id of the Log Analytics workspace.')
param workspaceId string

@description('Specifies the object id of a Miccrosoft Entra ID user. In general, this the object id of the system administrator who deploys the Azure resources.')
param userObjectId string

resource keyVault 'Microsoft.KeyVault/vaults@2022-07-01' = {
  name: keyvaultName
  location: location
  tags: tags
  properties: {
    createMode: 'default'
    enabledForDeployment: false
    enabledForDiskEncryption: false
    enabledForTemplateDeployment: false
    enableSoftDelete: true
    enableRbacAuthorization: true
    enablePurgeProtection: true
    networkAcls: {
      bypass: 'AzureServices'
      defaultAction: 'Deny'
    }
    sku: {
      family: 'A'
      name: 'standard'
    }
    softDeleteRetentionInDays: 7
    tenantId: subscription().tenantId
  }
}

resource keyVaultAdministratorRoleDefinition 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: '00482a5a-887f-4fb3-b363-3b7fe8e74483'
  scope: subscription()
}

// This role assignment grants the user the required permissions to perform all data plane operations Key Vault and all objects in it, including certificates, keys, and secrets.
resource keyVaultAdministratorUserRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(userObjectId)) {
  name: guid(keyVault.id, keyVaultAdministratorRoleDefinition.id, userObjectId)
  scope: keyVault
  properties: {
    roleDefinitionId: keyVaultAdministratorRoleDefinition.id
    principalType: 'User'
    principalId: userObjectId
  }
}

output keyVaultId string = keyVault.id
