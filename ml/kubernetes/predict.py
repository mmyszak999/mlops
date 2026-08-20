import os

import mlflow
import mlflow.pyfunc
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel


# =========================================================
# Configuration
# =========================================================

MLFLOW_TRACKING_URI = os.environ["MLFLOW_TRACKING_URI"]

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "titanic-random-forest"
)

MODEL_REGISTRY_VERSION = os.getenv(
    "MODEL_REGISTRY_VERSION",
    "1"
)


# =========================================================
# MLflow
# =========================================================

mlflow.set_tracking_uri(
    MLFLOW_TRACKING_URI
)


# =========================================================
# Load model from Model Registry
# =========================================================

MODEL_URI = (
    f"models:/{MODEL_NAME}/{MODEL_REGISTRY_VERSION}"
)

model = mlflow.pyfunc.load_model(
    MODEL_URI
)


# =========================================================
# Get model version information
# =========================================================

client = mlflow.MlflowClient()

model_version = client.get_model_version(
    name=MODEL_NAME,
    version=MODEL_REGISTRY_VERSION
)

run_id = model_version.run_id


# =========================================================
# Download columns.pkl from the same MLflow run
# =========================================================

columns_path = mlflow.artifacts.download_artifacts(
    run_id=run_id,
    artifact_path="columns.pkl"
)

columns = pd.read_pickle(
    columns_path
)


# =========================================================
# FastAPI
# =========================================================

app = FastAPI()


class PredictionRequest(BaseModel):
    Pclass: int
    Sex: str
    Age: float
    SibSp: int
    Parch: int
    Fare: float
    Embarked: str


# =========================================================
# Health check
# =========================================================

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_name": MODEL_NAME,
        "model_registry_version": MODEL_REGISTRY_VERSION
    }


# =========================================================
# Prediction
# =========================================================

@app.post("/predict")
def predict(request: PredictionRequest):

    data = {
        "Pclass": [request.Pclass],
        "Sex": [request.Sex],
        "Age": [request.Age],
        "SibSp": [request.SibSp],
        "Parch": [request.Parch],
        "Fare": [request.Fare],
        "Embarked": [request.Embarked]
    }

    df = pd.DataFrame(data)

    # Same preprocessing as during training
    df = pd.get_dummies(df)

    # Ensure exactly the same columns and column order
    # as during training.
    df = df.reindex(
        columns=columns,
        fill_value=0
    )

    prediction = model.predict(df)

    return {
        "prediction": int(prediction[0]),
        "model_name": MODEL_NAME,
        "model_registry_version": MODEL_REGISTRY_VERSION
    }