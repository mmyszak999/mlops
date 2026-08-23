#!/usr/bin/env bash

set -euo pipefail

TERRAFORM_DIR="terraform/kubernetes/aws"

echo "=========================================="
echo " AWS Kubernetes cleanup"
echo "=========================================="
echo
echo "This will destroy Terraform-managed AWS resources:"
echo
echo "  - EKS cluster"
echo "  - EKS node group"
echo "  - ECR repositories"
echo "  - S3 model bucket"
echo "  - IAM roles/policies"
echo "  - Pod Identity associations"
echo "  - VPC / subnets / networking"
echo "  - EKS add-ons"
echo
echo "This action is destructive."
echo

read -r -p "Type DESTROY to continue: " confirmation

if [[ "$confirmation" != "DESTROY" ]]; then
    echo
    echo "Cleanup cancelled."
    exit 0
fi

echo
echo "Running Terraform destroy..."
echo

terraform -chdir="$TERRAFORM_DIR" destroy -auto-approve

echo
echo "=========================================="
echo " Cleanup completed"
echo "=========================================="