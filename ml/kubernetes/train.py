import os

import mlflow
import mlflow.sklearn

from ml.core.data import load_data
from ml.core.model import (
    create_model,
    evaluate_model,
    train_model,
)
from ml.core.preprocessing import preprocess_data

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "titanic-random-forest",
)

MLFLOW_TRACKING_URI = os.environ[
    "MLFLOW_TRACKING_URI"
]

mlflow.set_tracking_uri(
    MLFLOW_TRACKING_URI
)

mlflow.set_experiment(
    "titanic",
)

df = load_data()

(
    X_train,
    X_test,
    y_train,
    y_test,
    feature_columns,
) = preprocess_data(df)

model = create_model()


with mlflow.start_run():

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

    mlflow.log_params(
        {
            "n_estimators": 200,
            "max_depth": 10,
            "min_samples_split": 5,
            "random_state": 42,
        }
    )

    mlflow.log_metric(
        "accuracy",
        accuracy,
    )

    joblib_path = "columns.pkl"

    import joblib

    joblib.dump(
        feature_columns,
        joblib_path,
    )

    mlflow.log_artifact(
        joblib_path,
    )

    mlflow.sklearn.log_model(
        model,
        name="model",
        registered_model_name=MODEL_NAME,
    )

    print(
        f"Model registered as "
        f"{MODEL_NAME}"
    )