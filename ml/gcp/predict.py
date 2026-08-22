import os

import joblib
import numpy as np

from google.cloud.aiplatform.prediction.predictor import Predictor
from google.cloud.aiplatform.utils import prediction_utils


class TitanicPredictor(Predictor):
    """
    Custom Vertex AI predictor for the Titanic model.
    """

    def __init__(self):
        self.model = None

    def load(self, artifacts_uri: str):
        """
        Download model artifacts from GCS
        and load the serialized sklearn pipeline.
        """

        prediction_utils.download_model_artifacts(
            artifacts_uri
        )

        self.model = joblib.load(
            "model.joblib"
        )

    def preprocess(
        self,
        prediction_input: dict,
    ) -> np.ndarray:
        """
        Convert Vertex AI request into model input.

        Expected request:

        {
            "instances": [
                {
                    "Pclass": 1,
                    "Sex": "female",
                    "Age": 12,
                    "SibSp": 0,
                    "Parch": 0,
                    "Fare": 1311.2833,
                    "Embarked": "Q"
                }
            ]
        }
        """

        return prediction_input["instances"]

    def predict(
        self,
        instances,
    ):
        """
        Run prediction using the complete sklearn pipeline.
        """

        predictions = self.model.predict(
            instances
        )

        return predictions

    def postprocess(
        self,
        prediction_results,
    ) -> dict:
        """
        Return JSON-serializable predictions.
        """

        return {
            "predictions": [
                int(value)
                for value in prediction_results
            ]
        }