import joblib
import pandas as pd

from google.cloud.aiplatform.prediction.predictor import Predictor
from google.cloud.aiplatform.utils import prediction_utils


class TitanicPredictor(Predictor):

    def __init__(self):
        self.model = None

    def load(self, artifacts_uri: str):
        prediction_utils.download_model_artifacts(
            artifacts_uri
        )

        self.model = joblib.load(
            "model.joblib"
        )

    def preprocess(self, prediction_input: dict):
        instances = prediction_input["instances"]

        columns = [
            "Pclass",
            "Sex",
            "Age",
            "SibSp",
            "Parch",
            "Fare",
            "Embarked",
        ]

        return pd.DataFrame(
            instances,
            columns=columns,
        )

    def predict(self, instances):
        return self.model.predict(
            instances
        )

    def postprocess(self, prediction_results):
        return {
            "predictions": [
                int(value)
                for value in prediction_results
            ]
        }