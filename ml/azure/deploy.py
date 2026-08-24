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
    "AZURE_SUBSCRIPTION_ID"
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

MODEL_VERSION = os.getenv(
    "MODEL_VERSION",
    "1",
)

ENDPOINT_NAME = os.getenv(
    "ENDPOINT_NAME",
    "titanic-random-forest",
)

DEPLOYMENT_NAME = os.getenv(
    "DEPLOYMENT_NAME",
    "blue",
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

print(
    f"Using model: "
    f"{model.name} v{model.version}"
)


# =========================================================
# Create endpoint
# =========================================================

endpoint = ManagedOnlineEndpoint(
    name=ENDPOINT_NAME,
    description="Titanic Random Forest endpoint",
    auth_mode="key",
)

print(
    f"Creating endpoint: "
    f"{ENDPOINT_NAME}"
)

endpoint = (
    ml_client.online_endpoints
    .begin_create_or_update(
        endpoint
    )
    .result()
)

print(
    f"Endpoint created: "
    f"{endpoint.name}"
)


# =========================================================
# Create deployment
# =========================================================

deployment = ManagedOnlineDeployment(
    name=DEPLOYMENT_NAME,
    endpoint_name=ENDPOINT_NAME,
    model=model,
    instance_type="Standard_DS2_v2",
    instance_count=1,
)

print(
    f"Creating deployment: "
    f"{DEPLOYMENT_NAME}"
)

deployment = (
    ml_client.online_deployments
    .begin_create_or_update(
        deployment
    )
    .result()
)

print(
    f"Deployment created: "
    f"{deployment.name}"
)


# =========================================================
# Route 100% traffic
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

print(
    "Traffic configured:"
)

print(
    endpoint.traffic
)

print(
    f"Scoring URI: "
    f"{endpoint.scoring_uri}"
)