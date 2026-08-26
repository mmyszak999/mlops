#!/usr/bin/env bash

set -euo pipefail

TERRAFORM_DIR="terraform/kubernetes/azure"

AZURE_RESOURCE_GROUP="mlops-thesis-aks"
AKS_CLUSTER_NAME="mlops-thesis-aks"

KUBERNETES_NAMESPACE="mlops"

echo "=========================================="
echo " Azure Kubernetes cleanup"
echo "=========================================="
echo

echo "This will destroy Terraform-managed Azure AKS resources:"
echo

echo "  - AKS cluster"
echo "  - AKS node pool"
echo "  - Azure Container Registry"
echo "  - Azure Storage Account"
echo "  - Storage containers"
echo "  - User Assigned Managed Identities"
echo "  - Federated Identity Credentials"
echo "  - Azure RBAC role assignments"
echo "  - Resource Group"
echo

echo "It will also remove Kubernetes workloads:"
echo

echo "  - MLflow"
echo "  - PostgreSQL"
echo "  - Inference Deployment"
echo "  - Inference Service"
echo "  - Training Jobs"
echo "  - Azure Workload Identity ServiceAccounts"
echo "  - PersistentVolumeClaims"
echo "  - Kubernetes namespace: ${KUBERNETES_NAMESPACE}"
echo

echo "WARNING: This action is destructive."
echo

read -r -p "Type DESTROY to continue: " confirmation

if [[ "$confirmation" != "DESTROY" ]]; then
    echo
    echo "Cleanup cancelled."
    exit 0
fi

echo
echo "=========================================="
echo " Step 1 - Get AKS credentials"
echo "=========================================="
echo

if az aks show \
    --resource-group "$AZURE_RESOURCE_GROUP" \
    --name "$AKS_CLUSTER_NAME" \
    >/dev/null 2>&1; then

    az aks get-credentials \
        --resource-group "$AZURE_RESOURCE_GROUP" \
        --name "$AKS_CLUSTER_NAME" \
        --overwrite-existing

else
    echo "AKS cluster does not exist."
    echo "Skipping Kubernetes cleanup."
fi

echo
echo "=========================================="
echo " Step 2 - Remove Kubernetes workloads"
echo "=========================================="
echo

if kubectl get namespace "$KUBERNETES_NAMESPACE" >/dev/null 2>&1; then

    echo "Deleting namespace: ${KUBERNETES_NAMESPACE}"
    echo

    kubectl delete namespace "$KUBERNETES_NAMESPACE" \
        --wait=true

    echo
    echo "Namespace deleted."

else
    echo "Namespace ${KUBERNETES_NAMESPACE} does not exist."
fi

echo
echo "=========================================="
echo " Step 3 - Terraform destroy"
echo "=========================================="
echo

terraform -chdir="$TERRAFORM_DIR" destroy -auto-approve

echo
echo "=========================================="
echo " Cleanup completed"
echo "=========================================="