import os

from azure.ai.ml import MLClient
from azure.ai.ml.entities import (
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
)
from azure.identity import DefaultAzureCredential


# =========================================================
# Configuration
# =========================================================

AZURE_SUBSCRIPTION_ID = os.environ[
    "ARM_SUBSCRIPTION_ID"
]

AZURE_RESOURCE_GROUP = os.environ[
    "AZURE_RESOURCE_GROUP"
]

AZURE_ML_WORKSPACE = os.environ[
    "AZURE_ML_WORKSPACE"
]

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "titanic-random-forest",
)

MODEL_VERSION = os.environ[
    "MODEL_VERSION"
]

ENDPOINT_NAME = os.getenv(
    "ENDPOINT_NAME",
    "titanic-random-forest",
)

DEPLOYMENT_NAME = os.getenv(
    "DEPLOYMENT_NAME",
    "blue",
)

INSTANCE_TYPE = os.getenv(
    "INSTANCE_TYPE",
    "Standard_DS3_v2",
)


# =========================================================
# Azure ML client
# =========================================================

credential = DefaultAzureCredential()

ml_client = MLClient(
    credential=credential,
    subscription_id=AZURE_SUBSCRIPTION_ID,
    resource_group_name=AZURE_RESOURCE_GROUP,
    workspace_name=AZURE_ML_WORKSPACE,
)


# =========================================================
# Get registered model
# =========================================================

model = ml_client.models.get(
    name=MODEL_NAME,
    version=MODEL_VERSION,
)

print("Using model:")

print(
    f"name={model.name}"
)

print(
    f"version={model.version}"
)

print(
    f"type={model.type}"
)


# =========================================================
# Create or update endpoint
# =========================================================

endpoint = ManagedOnlineEndpoint(
    name=ENDPOINT_NAME,
    description="Titanic Random Forest managed online endpoint",
    auth_mode="key",
)

print(
    f"Creating/updating endpoint: {ENDPOINT_NAME}"
)

endpoint = (
    ml_client.online_endpoints
    .begin_create_or_update(
        endpoint
    )
    .result()
)

print(
    f"Endpoint ready: {endpoint.name}"
)


# =========================================================
# Delete existing deployment
# =========================================================

print(
    f"Checking existing deployment: {DEPLOYMENT_NAME}"
)

try:
    ml_client.online_deployments.begin_delete(
        name=DEPLOYMENT_NAME,
        endpoint_name=ENDPOINT_NAME,
    ).result()

    print(
        f"Existing deployment deleted: "
        f"{DEPLOYMENT_NAME}"
    )

except Exception as exc:
    message = str(exc).lower()

    if (
        "not found" in message
        or "resourcenotfound" in message
    ):
        print(
            f"Deployment does not exist: "
            f"{DEPLOYMENT_NAME}"
        )
    else:
        raise


# =========================================================
# Create deployment
# =========================================================

deployment = ManagedOnlineDeployment(
    name=DEPLOYMENT_NAME,
    endpoint_name=ENDPOINT_NAME,
    model=model,
    instance_type=INSTANCE_TYPE,
    instance_count=1,
)

print(
    f"Creating deployment: {DEPLOYMENT_NAME}"
)

deployment = (
    ml_client.online_deployments
    .begin_create_or_update(
        deployment
    )
    .result()
)

print(
    f"Deployment ready: {deployment.name}"
)


# =========================================================
# Route traffic
# =========================================================

endpoint = ml_client.online_endpoints.get(
    ENDPOINT_NAME
)

endpoint.traffic = {
    DEPLOYMENT_NAME: 100
}

endpoint = (
    ml_client.online_endpoints
    .begin_create_or_update(
        endpoint
    )
    .result()
)


# =========================================================
# Output
# =========================================================

print(
    "Deployment completed."
)

print(
    f"Endpoint name: {endpoint.name}"
)

print(
    f"Deployment name: {DEPLOYMENT_NAME}"
)

print(
    f"Model version: {MODEL_VERSION}"
)

print(
    f"Scoring URI: {endpoint.scoring_uri}"
)