import os

import mlflow
import mlflow.pyfunc
import pandas as pd

from fastapi import FastAPI
from pydantic import BaseModel


MLFLOW_TRACKING_URI = os.environ[
    "MLFLOW_TRACKING_URI"
]

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "titanic-random-forest"
)

MODEL_VERSION = os.getenv(
    "MODEL_VERSION",
    "1"
)


mlflow.set_tracking_uri(
    MLFLOW_TRACKING_URI
)

model = mlflow.pyfunc.load_model(
    f"models:/{MODEL_NAME}/{MODEL_VERSION}"
)


app = FastAPI()


class PredictionRequest(BaseModel):
    Pclass: int
    Sex: str
    Age: float
    SibSp: int
    Parch: int
    Fare: float
    Embarked: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_version": MODEL_VERSION
    }


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

    df = pd.get_dummies(df)

    prediction = model.predict(df)

    return {
        "prediction": int(prediction[0]),
        "model_version": MODEL_VERSION
    }