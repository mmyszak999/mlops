resource "azurerm_resource_group" "mlops" {
  name     = var.resource_group_name
  location = var.location
}


resource "azurerm_storage_account" "ml" {
  name = "mlopsthesis${substr(
    md5(var.subscription_id),
    0,
    8
  )}"

  resource_group_name = azurerm_resource_group.mlops.name
  location            = azurerm_resource_group.mlops.location

  account_tier             = "Standard"
  account_replication_type = "LRS"

  min_tls_version = "TLS1_2"

  blob_properties {
    versioning_enabled = true
  }
}


resource "azurerm_key_vault" "ml" {
  name = "mlops-thesis-kv-${substr(
    md5(var.subscription_id),
    0,
    8
  )}"

  location            = azurerm_resource_group.mlops.location
  resource_group_name = azurerm_resource_group.mlops.name

  tenant_id = data.azurerm_client_config.current.tenant_id

  sku_name = "standard"

  rbac_authorization_enabled = true
}


resource "azurerm_application_insights" "ml" {
  name = "mlops-thesis-appinsights"

  location            = azurerm_resource_group.mlops.location
  resource_group_name = azurerm_resource_group.mlops.name

  application_type = "web"
}


resource "azurerm_machine_learning_workspace" "ml" {
  name                = var.workspace_name
  location            = azurerm_resource_group.mlops.location
  resource_group_name = azurerm_resource_group.mlops.name

  application_insights_id = azurerm_application_insights.ml.id
  key_vault_id            = azurerm_key_vault.ml.id
  storage_account_id      = azurerm_storage_account.ml.id

  identity {
    type = "SystemAssigned"
  }

  public_network_access_enabled = true
}