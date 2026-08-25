variable "subscription_id" {
  description = "Azure subscription ID."
  type        = string
  default     = "a71b1a56-760a-4510-9453-9525c3b99c8f"
}

variable "location" {
  description = "Azure region for AKS resources."
  type        = string
  default     = "polandcentral"
}

variable "resource_group_name" {
  description = "Resource group for the AKS platform."
  type        = string
  default     = "mlops-thesis-aks"
}

variable "cluster_name" {
  description = "AKS cluster name."
  type        = string
  default     = "mlops-thesis-aks"
}

variable "kubernetes_version" {
  description = "Optional AKS Kubernetes version. Leave null to use the default supported version."
  type        = string
  default     = null
  nullable    = true
}

variable "node_vm_size" {
  description = "AKS node VM size. Standard_B2s is intentionally small for the Azure for Students quota."
  type        = string
  default     = "Standard_B2s_v2"
}

variable "node_count" {
  description = "Initial AKS node count."
  type        = number
  default     = 1
}

variable "node_min_count" {
  description = "Minimum AKS node count when autoscaling is enabled."
  type        = number
  default     = 1
}

variable "node_max_count" {
  description = "Maximum AKS node count when autoscaling is enabled."
  type        = number
  default     = 2
}

variable "aks_dns_prefix" {
  description = "DNS prefix for AKS."
  type        = string
  default     = "mlops-thesis-aks"
}

variable "tags" {
  description = "Tags applied to Azure resources."
  type        = map(string)

  default = {
    project     = "mlops-thesis"
    environment = "kubernetes"
    managed_by  = "terraform"
  }
}