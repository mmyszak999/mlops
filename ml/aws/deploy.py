import os

import boto3
import sagemaker
from sagemaker.sklearn.model import SKLearnModel


# =========================================================
# Configuration
# =========================================================

AWS_REGION = os.environ["AWS_REGION"]

MODEL_BUCKET = os.environ["MODEL_BUCKET"]

SAGEMAKER_ROLE_ARN = os.environ[
    "SAGEMAKER_ROLE_ARN"
]

MODEL_VERSION = os.environ[
    "MODEL_VERSION"
]

ENDPOINT_NAME = os.environ[
    "ENDPOINT_NAME"
]

INSTANCE_TYPE = os.environ[
    "INSTANCE_TYPE"
]

FRAMEWORK_VERSION = os.environ[
    "FRAMEWORK_VERSION"
]

ENTRY_POINT = os.environ[
    "ENTRY_POINT"
]


# =========================================================
# AWS / SageMaker session
# =========================================================

boto_session = boto3.Session(
    region_name=AWS_REGION
)

session = sagemaker.Session(
    boto_session=boto_session
)


# =========================================================
# Model artifact
# =========================================================

model_data = (
    f"s3://{MODEL_BUCKET}/"
    f"models/{MODEL_VERSION}/model.tar.gz"
)

print("=== SageMaker deployment configuration ===")
print(f"AWS region: {AWS_REGION}")
print(f"Model bucket: {MODEL_BUCKET}")
print(f"Model version: {MODEL_VERSION}")
print(f"Model artifact: {model_data}")
print(f"Endpoint: {ENDPOINT_NAME}")
print(f"Instance type: {INSTANCE_TYPE}")
print(f"Framework version: {FRAMEWORK_VERSION}")
print(f"Entry point: {ENTRY_POINT}")


# =========================================================
# Create SageMaker model
# =========================================================

model = SKLearnModel(
    model_data=model_data,
    role=SAGEMAKER_ROLE_ARN,
    framework_version=FRAMEWORK_VERSION,
    entry_point=ENTRY_POINT,
    sagemaker_session=session,
)


# =========================================================
# Deploy endpoint
# =========================================================

print(
    f"Deploying model to endpoint: "
    f"{ENDPOINT_NAME}"
)

predictor = model.deploy(
    endpoint_name=ENDPOINT_NAME,
    initial_instance_count=1,
    instance_type=INSTANCE_TYPE,
)


# =========================================================
# Result
# =========================================================

print()
print("==========================================")
print(" SageMaker deployment completed")
print("==========================================")
print(f"Endpoint: {ENDPOINT_NAME}")
print(f"Model version: {MODEL_VERSION}")
print(f"Instance type: {INSTANCE_TYPE}")