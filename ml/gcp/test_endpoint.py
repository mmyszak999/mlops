import os

from google.cloud import aiplatform


PROJECT_ID = os.environ["GCP_PROJECT_ID"]

REGION = os.getenv(
    "GCP_REGION",
    "us-central1",
)

ENDPOINT_ID = os.environ[
    "VERTEX_ENDPOINT_ID"
]


aiplatform.init(
    project=PROJECT_ID,
    location=REGION,
)


endpoint = aiplatform.Endpoint(
    endpoint_name=ENDPOINT_ID
)


instances = [
    {
        "Pclass": 1,
        "Sex": "female",
        "Age": 12,
        "SibSp": 0,
        "Parch": 0,
        "Fare": 1311.2833,
        "Embarked": "Q",
    }
]


response = endpoint.predict(
    instances=instances
)


print(
    "Prediction response:"
)

print(
    response
)