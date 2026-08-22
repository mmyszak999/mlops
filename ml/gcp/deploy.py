import os

from google.cloud import aiplatform
from google.cloud.aiplatform.prediction import LocalModel

from ml.gcp.predict import TitanicPredictor


# =========================================================
# Configuration
# =========================================================

PROJECT_ID = os.environ[
    "GCP_PROJECT_ID"
]

REGION = os.getenv(
    "GCP_REGION",
    "us-central1",
)

MODEL_BUCKET = os.environ[
    "MODEL_BUCKET"
]

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

ARTIFACT_REGISTRY_URL = os.environ[
    "ARTIFACT_REGISTRY_URL"
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
    f"gs://{MODEL_BUCKET}/"
    f"models/{MODEL_VERSION}"
)

print(
    f"Model artifact URI: {artifact_uri}"
)


# =========================================================
# Serving image
# =========================================================

image_uri = (
    f"{ARTIFACT_REGISTRY_URL}/"
    f"{MODEL_DISPLAY_NAME}:{MODEL_VERSION}"
)

print(
    f"Serving image URI: {image_uri}"
)


# =========================================================
# Build Custom Prediction Routine
# =========================================================

local_model = LocalModel.build_cpr_model(
    src_dir="ml/gcp",
    output_image_uri=image_uri,
    predictor=TitanicPredictor,
    requirements_path="ml/gcp/requirements.txt",
    platform="linux/amd64",
    base_image="python:3.11-slim",
)

print(
    "Custom Prediction Routine built."
)


# =========================================================
# Push serving image
# =========================================================

local_model.push_image()

print(
    "Serving image pushed to Artifact Registry."
)


# =========================================================
# Upload model to Vertex Model Registry
# =========================================================

model = aiplatform.Model.upload(
    local_model=local_model,
    display_name=MODEL_DISPLAY_NAME,
    artifact_uri=artifact_uri,
)

model.wait()

print(
    f"Vertex model created: "
    f"{model.resource_name}"
)


# =========================================================
# Create endpoint
# =========================================================

endpoint = aiplatform.Endpoint.create(
    display_name=ENDPOINT_DISPLAY_NAME,
)

endpoint.wait()

print(
    f"Vertex endpoint created: "
    f"{endpoint.resource_name}"
)


# =========================================================
# Deploy model
# =========================================================

print(
    f"Deploying model to endpoint: "
    f"{endpoint.resource_name}"
)

model.deploy(
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
# GitHub Actions output
# =========================================================

github_output = os.getenv(
    "GITHUB_OUTPUT"
)

if github_output:
    with open(
        github_output,
        "a",
        encoding="utf-8",
    ) as file:
        file.write(
            f"endpoint_id={endpoint.name}\n"
        )