#!/usr/bin/env bash

set -euo pipefail

TERRAFORM_DIR="terraform/kubernetes/gcp"

echo "=========================================="
echo " GCP Kubernetes cleanup"
echo "=========================================="
echo

echo "This will destroy Terraform-managed GCP resources:"
echo
echo "  - GKE cluster"
echo "  - GKE node pool"
echo "  - Artifact Registry repository"
echo "  - GCS model bucket"
echo "  - Google Service Accounts"
echo "  - IAM roles and Workload Identity bindings"
echo "  - VPC / subnet / networking"
echo "  - GKE-related resources"
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