terraform {
  required_version = ">= 1.6.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.45"
    }
  }

  backend "azurerm" {
    resource_group_name  = "mlops-terraform-state"
    storage_account_name = "mlopstfstateazure"
    container_name       = "tfstate"
    key                  = "azure-native.tfstate"
  }
}