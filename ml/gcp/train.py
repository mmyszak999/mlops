import os

import joblib
import pandas as pd
from google.cloud import storage

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


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

df = pd.read_csv(
    "data/data.csv"
)


# =========================================================
# Preprocessing
# =========================================================

df["Age"] = df["Age"].fillna(
    df["Age"].median()
)

df["Embarked"] = df["Embarked"].fillna(
    df["Embarked"].mode()[0]
)


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


X = pd.get_dummies(
    X
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
# Model
# =========================================================

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    min_samples_split=5,
    random_state=42,
)


model.fit(
    X_train,
    y_train,
)


# =========================================================
# Evaluation
# =========================================================

predictions = model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions,
)

print(
    f"Model accuracy: {accuracy:.4f}"
)


# =========================================================
# Save artifacts locally
# =========================================================

model_filename = "model.pkl"
columns_filename = "columns.pkl"

joblib.dump(
    model,
    model_filename,
)

joblib.dump(
    X.columns.tolist(),
    columns_filename,
)


# =========================================================
# Upload artifacts to GCS
# =========================================================

storage_client = storage.Client(
    project=GCP_PROJECT_ID
)

bucket = storage_client.bucket(
    MODEL_BUCKET
)


model_blob = bucket.blob(
    f"models/{MODEL_VERSION}/{model_filename}"
)

model_blob.upload_from_filename(
    model_filename
)


columns_blob = bucket.blob(
    f"models/{MODEL_VERSION}/{columns_filename}"
)

columns_blob.upload_from_filename(
    columns_filename
)


print(
    "Model artifacts uploaded successfully:"
)

print(
    f"gs://{MODEL_BUCKET}/models/{MODEL_VERSION}/{model_filename}"
)

print(
    f"gs://{MODEL_BUCKET}/models/{MODEL_VERSION}/{columns_filename}"
)