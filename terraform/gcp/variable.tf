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

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "mlops-project"
}