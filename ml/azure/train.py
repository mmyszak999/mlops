import os

import mlflow
import mlflow.sklearn

from azure.ai.ml import MLClient
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
    "ARM_SUBSCRIPTION_ID"
]

AZURE_RESOURCE_GROUP = os.environ[
    "AZURE_RESOURCE_GROUP"
]

AZURE_ML_WORKSPACE = os.environ[
    "AZURE_ML_WORKSPACE"
]

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "titanic-random-forest",
)

MODEL_VERSION = os.getenv(
    "MODEL_VERSION",
    "1",
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
# MLflow tracking
# =========================================================

workspace = ml_client.workspaces.get(
    AZURE_ML_WORKSPACE
)

mlflow.set_tracking_uri(
    workspace.mlflow_tracking_uri
)

mlflow.set_experiment(
    "titanic"
)


# =========================================================
# Load data
# =========================================================

df = load_data()


# =========================================================
# Preprocessing
# =========================================================

(
    X_train,
    X_test,
    y_train,
    y_test,
    feature_columns,
) = preprocess_data(
    df
)


# =========================================================
# Train model
# =========================================================

model = create_model()

model = train_model(
    model,
    X_train,
    y_train,
)


# =========================================================
# Evaluation
# =========================================================

accuracy = evaluate_model(
    model,
    X_test,
    y_test,
)

print(
    f"Model accuracy: {accuracy:.4f}"
)


# =========================================================
# MLflow run
# =========================================================

with mlflow.start_run() as run:

    mlflow.log_param(
        "model_version",
        MODEL_VERSION,
    )

    mlflow.log_param(
        "model_name",
        MODEL_NAME,
    )

    mlflow.log_metric(
        "accuracy",
        accuracy,
    )

    mlflow.log_param(
        "n_features",
        len(feature_columns),
    )

    # MLflow 2.16.x compatible API
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
    )

    run_id = run.info.run_id

    print(
        f"MLflow run ID: {run_id}"
    )


# =========================================================
# Register model in Azure ML / MLflow Registry
# =========================================================

registered_model = mlflow.register_model(
    model_uri=f"runs:/{run_id}/model",
    name=MODEL_NAME,
)

print(
    "Model registered successfully:"
)

print(
    f"model_name={registered_model.name}"
)

print(
    f"model_version={registered_model.version}"
)