import os

import joblib
import pandas as pd

from google.cloud.aiplatform.prediction.predictor import Predictor
from google.cloud.aiplatform.utils import prediction_utils


class TitanicPredictor(Predictor):
    """
    Custom Prediction Routine for the Titanic model.

    Vertex AI calls:
        load()
        preprocess()
        predict()
        postprocess()
    """

    def __init__(self):
        self.model = None
        self.columns = None

    def load(self, artifacts_uri: str) -> None:
        """
        Download model artifacts from GCS and load them into memory.
        """

        prediction_utils.download_model_artifacts(
            artifacts_uri
        )

        self.model = joblib.load(
            os.path.join(
                "model.pkl"
            )
        )

        self.columns = joblib.load(
            os.path.join(
                "columns.pkl"
            )
        )

    def preprocess(self, prediction_input: dict):
        """
        Vertex receives:
        {
            "instances": [...]
        }

        Return only the instances for prediction.
        """

        return prediction_input["instances"]

    def predict(self, instances):
        """
        Convert input instances to the same feature representation
        that was used during training.
        """

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

    def postprocess(self, prediction_results):
        """
        Convert predictions into a JSON-serializable response.
        """

        return {
            "predictions": [
                int(value)
                for value in prediction_results
            ]
        }