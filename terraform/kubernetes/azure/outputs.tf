output "resource_group_name" {
  value = azurerm_resource_group.this.name
}

output "cluster_name" {
  value = azurerm_kubernetes_cluster.this.name
}

output "cluster_region" {
  value = azurerm_kubernetes_cluster.this.location
}

output "cluster_id" {
  value = azurerm_kubernetes_cluster.this.id
}

output "cluster_fqdn" {
  value = azurerm_kubernetes_cluster.this.fqdn
}

output "acr_name" {
  value = azurerm_container_registry.this.name
}

output "acr_login_server" {
  value = azurerm_container_registry.this.login_server
}

output "model_storage_account_name" {
  value = azurerm_storage_account.models.name
}

output "model_storage_container" {
  value = azurerm_storage_container.models.name
}

output "mlflow_storage_container" {
  value = azurerm_storage_container.mlflow.name
}

output "training_identity_client_id" {
  value = azurerm_user_assigned_identity.training.client_id
}

output "training_identity_principal_id" {
  value = azurerm_user_assigned_identity.training.principal_id
}

output "inference_identity_client_id" {
  value = azurerm_user_assigned_identity.inference.client_id
}

output "inference_identity_principal_id" {
  value = azurerm_user_assigned_identity.inference.principal_id
}

output "mlflow_identity_client_id" {
  value = azurerm_user_assigned_identity.mlflow.client_id
}

output "mlflow_identity_principal_id" {
  value = azurerm_user_assigned_identity.mlflow.principal_id
}

output "storage_class_name" {
  value = "managed-csi"
}