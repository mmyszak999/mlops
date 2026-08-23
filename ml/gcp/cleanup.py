import os

from google.cloud import aiplatform


PROJECT_ID = os.environ.get(
    "GCP_PROJECT_ID",
    "project-6e2348ec-04b1-4ad0-9e5",
)

REGION = os.environ.get(
    "GCP_REGION",
    "us-central1",
)

MODEL_DISPLAY_NAME = os.environ.get(
    "MODEL_DISPLAY_NAME",
    "titanic-random-forest",
)

ENDPOINT_DISPLAY_NAME = os.environ.get(
    "ENDPOINT_DISPLAY_NAME",
    "titanic-random-forest-endpoint",
)


# =========================================================
# Initialize Vertex AI
# =========================================================

aiplatform.init(
    project=PROJECT_ID,
    location=REGION,
)


# =========================================================
# Delete endpoint
# =========================================================

print(
    f"Searching for endpoint: "
    f"{ENDPOINT_DISPLAY_NAME}"
)

endpoints = aiplatform.Endpoint.list(
    filter=(
        f'display_name="{ENDPOINT_DISPLAY_NAME}"'
    )
)

for endpoint in endpoints:
    try:
        endpoint.undeploy_all()
        print(
            f"Undeployed all models from: "
            f"{endpoint.resource_name}"
        )
    except Exception as e:
        print(
            f"Undeploy error for "
            f"{endpoint.resource_name}: {e}"
        )

    try:
        endpoint.delete(
            force=True
        )
        print(
            f"Endpoint deleted: "
            f"{endpoint.resource_name}"
        )
    except Exception as e:
        print(
            f"Endpoint delete error for "
            f"{endpoint.resource_name}: {e}"
        )


# =========================================================
# Delete models
# =========================================================

print(
    f"Searching for models: "
    f"{MODEL_DISPLAY_NAME}"
)

models = aiplatform.Model.list(
    filter=(
        f'display_name="{MODEL_DISPLAY_NAME}"'
    )
)

for model in models:
    try:
        model.delete(
            force=True
        )

        print(
            f"Model deleted: "
            f"{model.resource_name}"
        )

    except Exception as e:
        print(
            f"Model delete error for "
            f"{model.resource_name}: {e}"
        )


print("GCP Vertex AI cleanup completed.")