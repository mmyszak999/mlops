import joblib

model = joblib.load("model.pkl")

def predict_fn(input_data, model):
    return model.predict(input_data)