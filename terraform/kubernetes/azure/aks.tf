resource "azurerm_kubernetes_cluster" "this" {
  name                = var.cluster_name
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  dns_prefix          = var.aks_dns_prefix

  kubernetes_version                 = var.kubernetes_version
  role_based_access_control_enabled  = true
  oidc_issuer_enabled                = true
  workload_identity_enabled          = true

  default_node_pool {
    name                 = "system"
    vm_size              = var.node_vm_size
    node_count           = var.node_count
    auto_scaling_enabled  = true
    min_count             = var.node_min_count
    max_count             = var.node_max_count

    os_disk_size_gb = 64
    type             = "VirtualMachineScaleSets"
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    load_balancer_sku = "standard"
    network_policy    = "azure"
  }

  tags = var.tags
}