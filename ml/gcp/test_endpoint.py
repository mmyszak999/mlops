import os

from google.cloud import aiplatform


PROJECT_ID = os.environ["GCP_PROJECT_ID"]

REGION = os.getenv(
    "GCP_REGION",
    "us-central1",
)

ENDPOINT_ID = os.environ["VERTEX_ENDPOINT_ID"]


# =========================================================
# Initialize Vertex AI
# =========================================================

aiplatform.init(
    project=PROJECT_ID,
    location=REGION,
)


# =========================================================
# Endpoint
# =========================================================

endpoint = aiplatform.Endpoint(
    endpoint_name=ENDPOINT_ID
)


# =========================================================
# Test instances
# =========================================================
#
# Order must match the raw feature order used by
# the GCP preprocessing pipeline:
#
# Pclass
# Sex
# Age
# SibSp
# Parch
# Fare
# Embarked
#

instances = [
    [
        1,
        "female",
        12,
        0,
        0,
        1311.2833,
        "Q",
    ],
    [
        3,
        "male",
        45,
        0,
        0,
        7.25,
        "S",
    ],
]


# =========================================================
# Prediction
# =========================================================

response = endpoint.predict(
    instances=instances
)


# =========================================================
# Output
# =========================================================

print("Vertex AI prediction response:")
print(response)