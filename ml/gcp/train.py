import os

import joblib
from google.cloud import storage

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from ml.core.data import load_data
from ml.core.model import (
    create_model,
    evaluate_model,
)
from ml.core.pipeline_preprocessing import (
    create_preprocessor,
)


# =========================================================
# Configuration
# =========================================================

MODEL_VERSION = os.getenv(
    "MODEL_VERSION",
    "v1",
)

GCP_PROJECT_ID = os.environ[
    "GCP_PROJECT_ID"
]

MODEL_BUCKET = os.environ[
    "MODEL_BUCKET"
]


# =========================================================
# Load data
# =========================================================

df = load_data(
    "data/data.csv"
)


# =========================================================
# Separate target and features
# =========================================================

y = df["Survived"]

X = df.drop(
    columns=[
        "PassengerId",
        "Survived",
        "Name",
        "Ticket",
        "Cabin",
    ]
)


# =========================================================
# Train / test split
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)


# =========================================================
# Build complete ML pipeline
# =========================================================

model_pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            create_preprocessor(),
        ),
        (
            "model",
            create_model(),
        ),
    ]
)


# =========================================================
# Train
# =========================================================

model_pipeline.fit(
    X_train,
    y_train,
)


# =========================================================
# Evaluation
# =========================================================

accuracy = evaluate_model(
    model_pipeline,
    X_test,
    y_test,
)

print(
    f"Model accuracy: {accuracy:.4f}"
)


# =========================================================
# Save complete model
# =========================================================

model_filename = "model.pkl"

joblib.dump(
    model_pipeline,
    model_filename,
)


# =========================================================
# Upload to GCS
# =========================================================

storage_client = storage.Client(
    project=GCP_PROJECT_ID,
)

bucket = storage_client.bucket(
    MODEL_BUCKET,
)

blob = bucket.blob(
    f"models/{MODEL_VERSION}/{model_filename}"
)

blob.upload_from_filename(
    model_filename,
)


print(
    "Model uploaded successfully:"
)

print(
    f"gs://{MODEL_BUCKET}/models/"
    f"{MODEL_VERSION}/{model_filename}"
)