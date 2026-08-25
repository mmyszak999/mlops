import os

from azure.ai.ml import MLClient
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

ENDPOINT_NAME = os.getenv(
    "ENDPOINT_NAME",
    "titanic-random-forest",
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
# Delete endpoint
# =========================================================

print(
    f"Deleting endpoint: "
    f"{ENDPOINT_NAME}"
)

try:
    operation = (
        ml_client.online_endpoints
        .begin_delete(
            ENDPOINT_NAME
        )
    )

    operation.result()

    print(
        f"Endpoint deleted: "
        f"{ENDPOINT_NAME}"
    )

except Exception as exc:
    message = str(exc)

    if (
        "ResourceNotFound" in message
        or "not found" in message.lower()
    ):
        print(
            f"Endpoint does not exist: "
            f"{ENDPOINT_NAME}"
        )
    else:
        raise


print(
    "Azure ML native cleanup completed."
)