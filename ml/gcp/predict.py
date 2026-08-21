import os

import joblib
import numpy as np

from google.cloud.aiplatform.prediction.predictor import Predictor
from google.cloud.aiplatform.utils import prediction_utils


class TitanicPredictor(Predictor):

    def __init__(self):
        self.model = None
        self.columns = None


    def load(self, artifacts_uri: str):

        prediction_utils.download_model_artifacts(
            artifacts_uri
        )

        self.model = joblib.load(
            "model.pkl"
        )

        self.columns = joblib.load(
            "columns.pkl"
        )


    def preprocess(
        self,
        prediction_input: dict,
    ):

        instances = prediction_input[
            "instances"
        ]

        return instances


    def predict(
        self,
        instances,
    ):

        import pandas as pd

        df = pd.DataFrame(
            instances
        )

        df = pd.get_dummies(
            df
        )

        df = df.reindex(
            columns=self.columns,
            fill_value=0,
        )

        predictions = self.model.predict(
            df
        )

        return predictions


    def postprocess(
        self,
        prediction_results,
    ):

        return {
            "predictions": [
                int(value)
                for value in prediction_results
            ]
        }