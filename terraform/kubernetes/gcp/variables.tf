variable "project_id" {
  description = "GCP project ID"
  type        = string
  default     = "project-6e2348ec-04b1-4ad0-9e5"
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "GCP zone"
  type        = string
  default     = "us-central1-a"
}

variable "cluster_name" {
  description = "GKE cluster name"
  type        = string
  default     = "mlops-thesis-gke"
}

variable "node_machine_type" {
  description = "GKE node machine type"
  type        = string
  default     = "e2-standard-2"
}