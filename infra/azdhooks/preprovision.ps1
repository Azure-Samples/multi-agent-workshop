Write-Host "Running preprovision.ps1"

if ($? -eq $true) {
    $myPrincipal = az ad signed-in-user show --query "id" -o tsv
    azd env set MY_USER_ID $myPrincipal
}
Write-Host "Finished executing preprovision.ps1"

 