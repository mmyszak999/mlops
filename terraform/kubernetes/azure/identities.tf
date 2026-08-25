resource "azurerm_user_assigned_identity" "training" {
  name                = local.training_identity_name
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location

  tags = var.tags
}

resource "azurerm_user_assigned_identity" "inference" {
  name                = local.inference_identity_name
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location

  tags = var.tags
}

resource "azurerm_user_assigned_identity" "mlflow" {
  name                = local.mlflow_identity_name
  resource_group_name = azurerm_resource_group.this.name
  location            = azurerm_resource_group.this.location

  tags = var.tags
}


resource "azurerm_federated_identity_credential" "training" {
  name = "training"

  parent_id = azurerm_user_assigned_identity.training.id

  issuer = azurerm_kubernetes_cluster.this.oidc_issuer_url

  subject = "system:serviceaccount:mlops:training"

  audience = [
    "api://AzureADTokenExchange",
  ]
}


resource "azurerm_federated_identity_credential" "inference" {
  name = "inference"

  parent_id = azurerm_user_assigned_identity.inference.id

  issuer = azurerm_kubernetes_cluster.this.oidc_issuer_url

  subject = "system:serviceaccount:mlops:inference"

  audience = [
    "api://AzureADTokenExchange",
  ]
}


resource "azurerm_federated_identity_credential" "mlflow" {
  name = "mlflow"

  parent_id = azurerm_user_assigned_identity.mlflow.id

  issuer = azurerm_kubernetes_cluster.this.oidc_issuer_url

  subject = "system:serviceaccount:mlops:mlflow"

  audience = [
    "api://AzureADTokenExchange",
  ]
}