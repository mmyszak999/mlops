# AKS kubelet identity needs permission to pull images from ACR.
resource "azurerm_role_assignment" "aks_acr_pull" {
  scope                = azurerm_container_registry.this.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_kubernetes_cluster.this.kubelet_identity[0].object_id
}

# Training workload: read/write model artifacts.
resource "azurerm_role_assignment" "training_blob" {
  scope                = azurerm_storage_account.models.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_user_assigned_identity.training.principal_id
}

# Inference workload: read model artifacts only.
resource "azurerm_role_assignment" "inference_blob" {
  scope                = azurerm_storage_account.models.id
  role_definition_name = "Storage Blob Data Reader"
  principal_id         = azurerm_user_assigned_identity.inference.principal_id
}

# MLflow workload: read/write artifacts.
resource "azurerm_role_assignment" "mlflow_blob" {
  scope                = azurerm_storage_account.models.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_user_assigned_identity.mlflow.principal_id
}