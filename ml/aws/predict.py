import json
import os
import joblib
import pandas as pd


def model_fn(model_dir):
    model = joblib.load(
        os.path.join(model_dir, "model.pkl")
    )

    columns = joblib.load(
        os.path.join(model_dir, "columns.pkl")
    )

    return {
        "model": model,
        "columns": columns,
    }


def input_fn(request_body, request_content_type):
    if request_content_type == "application/json":
        return json.loads(request_body)

    raise ValueError(
        f"Unsupported content type: {request_content_type}"
    )


def predict_fn(input_data, model_data):
    model = model_data["model"]
    columns = model_data["columns"]

    df = pd.DataFrame([input_data])

    df = pd.get_dummies(df)

    df = df.reindex(
        columns=columns,
        fill_value=0
    )

    prediction = model.predict(df)

    return int(prediction[0])


def output_fn(prediction, response_content_type):
    if response_content_type == "application/json":
        return json.dumps({
            "prediction": prediction
        })

    raise ValueError(
        f"Unsupported response type: {response_content_type}"
    )