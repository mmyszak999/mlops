output "subscription_id" {
  value = var.subscription_id
}

output "resource_group_name" {
  value = azurerm_resource_group.mlops.name
}

output "workspace_name" {
  value = azurerm_machine_learning_workspace.ml.name
}

output "location" {
  value = azurerm_machine_learning_workspace.ml.location
}

output "storage_account_name" {
  value = azurerm_storage_account.ml.name
}

output "storage_account_id" {
  value = azurerm_storage_account.ml.id
}

output "workspace_id" {
  value = azurerm_machine_learning_workspace.ml.id
}