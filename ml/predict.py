import joblib

def model_fn(model_dir):
    model = joblib.load(f"{model_dir}/model.pkl")
    return model

def predict_fn(input_data, model):
    prediction = model.predict(input_data)
    return prediction