import os

import mlflow
import mlflow.sklearn

from azure.ai.ml import MLClient
from azure.ai.ml.entities import Model
from azure.ai.ml.constants import AssetTypes
from azure.identity import DefaultAzureCredential

from ml.core.data import load_data
from ml.core.preprocessing import preprocess_data
from ml.core.model import (
    create_model,
    train_model,
    evaluate_model,
)


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

MODEL_VERSION = os.getenv(
    "MODEL_VERSION",
    "1",
)

MODEL_NAME = os.getenv(
    "MODEL_NAME",
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
# Load data
# =========================================================

df = load_data(
    "data/data.csv"
)


# =========================================================
# Preprocessing
# =========================================================

X, y = preprocess_data(
    df
)


# =========================================================
# Train model
# =========================================================

model = create_model()

model = train_model(
    model,
    X,
    y,
)


# =========================================================
# Evaluation
# =========================================================

accuracy = evaluate_model(
    model,
    X,
    y,
)

print(
    f"Model accuracy: {accuracy:.4f}"
)


# =========================================================
# MLflow
# =========================================================

mlflow.set_tracking_uri(
    ml_client.workspaces.get(
        AZURE_ML_WORKSPACE
    ).mlflow_tracking_uri
)

mlflow.set_experiment(
    "titanic"
)

with mlflow.start_run() as run:

    mlflow.log_param(
        "model_version",
        MODEL_VERSION,
    )

    mlflow.log_metric(
        "accuracy",
        accuracy,
    )

    mlflow.sklearn.log_model(
        model,
        name="model",
    )

    run_id = run.info.run_id

    print(
        f"MLflow run: {run_id}"
    )


# =========================================================
# Register MLflow model
# =========================================================

model_asset = Model(
    path=f"runs:/{run_id}/model",
    name=MODEL_NAME,
    type=AssetTypes.MLFLOW_MODEL,
)

registered_model = ml_client.models.create_or_update(
    model_asset
)

print(
    "Model registered:"
)

print(
    f"name={registered_model.name}"
)

print(
    f"version={registered_model.version}"
)