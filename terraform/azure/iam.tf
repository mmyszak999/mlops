resource "azurerm_role_assignment" "workspace_storage" {
  scope                = azurerm_storage_account.ml.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id = azurerm_machine_learning_workspace.ml.identity[0].principal_id
}
