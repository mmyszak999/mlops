terraform {
  backend "azurerm" {
    resource_group_name  = "mlops-terraform-state"
    storage_account_name = "mlopstfstateazure"
    container_name       = "tfstate"
    key                  = "azure-k8s.tfstate"
    use_azuread_auth     = true
  }
}