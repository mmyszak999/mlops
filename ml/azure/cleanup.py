import os

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential


AZURE_SUBSCRIPTION_ID = os.environ[
    "AZURE_SUBSCRIPTION_ID"
]

AZURE_RESOURCE_GROUP = os.environ[
    "AZURE_RESOURCE_GROUP"
]

AZURE_ML_WORKSPACE = os.environ[
    "AZURE_ML_WORKSPACE"
]

ENDPOINT_NAME = os.getenv(
    "ENDPOINT_NAME",
    "titanic-random-forest",
)


credential = DefaultAzureCredential()

ml_client = MLClient(
    credential=credential,
    subscription_id=AZURE_SUBSCRIPTION_ID,
    resource_group_name=AZURE_RESOURCE_GROUP,
    workspace_name=AZURE_ML_WORKSPACE,
)


try:
    ml_client.online_endpoints.begin_delete(
        ENDPOINT_NAME,
        delete_deployments=True,
    ).result()

    print(
        f"Endpoint deleted: {ENDPOINT_NAME}"
    )

except Exception as e:
    print(
        f"Endpoint delete error: {e}"
    )