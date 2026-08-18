variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "mlops-thesis-k8s"
}

variable "eks_cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "mlops-thesis-k8s"
}

variable "eks_version" {
  description = "Kubernetes version used by EKS"
  type        = string
  default     = "1.35"
}

variable "vpc_cidr" {
  description = "VPC CIDR"
  type        = string
  default     = "10.0.0.0/16"
}

variable "node_instance_types" {
  description = "EC2 instance types for EKS managed node group"
  type        = list(string)
  default     = ["t3.medium"]
}

variable "node_desired_size" {
  description = "Desired number of worker nodes"
  type        = number
  default     = 1
}

variable "node_min_size" {
  description = "Minimum number of worker nodes"
  type        = number
  default     = 1
}

variable "node_max_size" {
  description = "Maximum number of worker nodes"
  type        = number
  default     = 2
}

variable "force_destroy_model_bucket" {
  description = "Allow Terraform to delete model bucket even if it contains objects"
  type        = bool
  default     = true
}