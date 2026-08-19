import os
import tarfile

import boto3
import joblib

from ml.core.data import load_data
from ml.core.model import (
    create_model,
    evaluate_model,
    train_model,
)
from ml.core.preprocessing import preprocess_data


MODEL_VERSION = os.getenv(
    "MODEL_VERSION",
    "v1",
)

MODEL_BUCKET = os.environ[
    "MODEL_BUCKET"
]

df = load_data()

(
    X_train,
    X_test,
    y_train,
    y_test,
    feature_columns,
) = preprocess_data(df)

model = create_model()

train_model(
    model,
    X_train,
    y_train,
)

accuracy = evaluate_model(
    model,
    X_test,
    y_test,
)

print(
    f"Model accuracy: {accuracy:.4f}"
)

joblib.dump(
    model,
    "model.pkl",
)

joblib.dump(
    feature_columns,
    "columns.pkl",
)


with tarfile.open(
    "model.tar.gz",
    "w:gz",
) as tar:
    tar.add("model.pkl")
    tar.add("columns.pkl")

s3 = boto3.client(
    "s3",
)

s3_key = (
    f"models/"
    f"{MODEL_VERSION}/"
    f"model.tar.gz"
)

s3.upload_file(
    "model.tar.gz",
    MODEL_BUCKET,
    s3_key,
)

print(
    f"Model {MODEL_VERSION} uploaded "
    f"to s3://{MODEL_BUCKET}/{s3_key}"
)