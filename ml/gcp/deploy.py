import os

from google.cloud import aiplatform


PROJECT_ID = os.environ["GCP_PROJECT_ID"]

REGION = os.getenv(
    "GCP_REGION",
    "us-central1",
)

MODEL_BUCKET = os.environ["MODEL_BUCKET"]

MODEL_VERSION = os.getenv(
    "MODEL_VERSION",
    "v1",
)

MODEL_DISPLAY_NAME = os.getenv(
    "MODEL_DISPLAY_NAME",
    "titanic-random-forest",
)

ENDPOINT_DISPLAY_NAME = os.getenv(
    "ENDPOINT_DISPLAY_NAME",
    "titanic-random-forest-endpoint",
)

SERVING_CONTAINER_IMAGE_URI = os.environ[
    "SERVING_CONTAINER_IMAGE_URI"
]


# =========================================================
# Initialize Vertex AI
# =========================================================

aiplatform.init(
    project=PROJECT_ID,
    location=REGION,
)


# =========================================================
# Model artifacts
# =========================================================

artifact_uri = (
    f"gs://{MODEL_BUCKET}"
    f"/models/{MODEL_VERSION}"
)


# =========================================================
# Upload model to Vertex Model Registry
# =========================================================

model = aiplatform.Model.upload(
    display_name=MODEL_DISPLAY_NAME,
    artifact_uri=artifact_uri,
    serving_container_image_uri=SERVING_CONTAINER_IMAGE_URI,
)

model.wait()

print(
    f"Model uploaded: {model.resource_name}"
)


# =========================================================
# Create endpoint
# =========================================================

endpoint = aiplatform.Endpoint.create(
    display_name=ENDPOINT_DISPLAY_NAME,
)

endpoint.wait()

print(
    f"Endpoint created: {endpoint.resource_name}"
)


# =========================================================
# Deploy model
# =========================================================

endpoint.deploy(
    model,
    deployed_model_display_name=MODEL_DISPLAY_NAME,
    machine_type="e2-standard-2",
    min_replica_count=1,
    max_replica_count=1,
)

print(
    "Model deployed successfully."
)

print(
    f"Endpoint: {endpoint.resource_name}"
)