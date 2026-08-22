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


# =========================================================
# Initialize Vertex AI
# =========================================================

aiplatform.init(
    project=PROJECT_ID,
    location=REGION,
)


# =========================================================
# Model artifact
# =========================================================

artifact_uri = (
    f"gs://{MODEL_BUCKET}"
    f"/models/{MODEL_VERSION}"
)

print(
    f"Model artifact URI: {artifact_uri}"
)


# =========================================================
# Prebuilt scikit-learn serving container
# =========================================================

SERVING_CONTAINER_IMAGE_URI = (
    "us-docker.pkg.dev/"
    "vertex-ai/prediction/"
    "sklearn-cpu.1-4:latest"
)


# =========================================================
# Upload model to Vertex AI Model Registry
# =========================================================

model = aiplatform.Model.upload(
    display_name=MODEL_DISPLAY_NAME,
    artifact_uri=artifact_uri,
    serving_container_image_uri=SERVING_CONTAINER_IMAGE_URI,
)

model.wait()

print(
    f"Vertex model created: {model.resource_name}"
)


# =========================================================
# Create endpoint
# =========================================================

endpoint = aiplatform.Endpoint.create(
    display_name=ENDPOINT_DISPLAY_NAME,
)

endpoint.wait()

print(
    f"Vertex endpoint created: {endpoint.resource_name}"
)


# =========================================================
# Deploy model
# =========================================================

endpoint = model.deploy(
    endpoint=endpoint,
    machine_type="e2-standard-2",
    min_replica_count=1,
    max_replica_count=1,
)

print(
    "Model deployed successfully."
)

print(
    f"Endpoint ID: {endpoint.name}"
)


# =========================================================
# Export endpoint ID for GitHub Actions
# =========================================================

github_output = os.getenv("GITHUB_OUTPUT")

if github_output:
    with open(github_output, "a", encoding="utf-8") as file:
        file.write(
            f"endpoint_id={endpoint.name}\n"
        )