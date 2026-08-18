from pathlib import Path

import pandas as pd


DATASET_PATH = Path("data/data.csv")


def load_data() -> pd.DataFrame:
    """
    Load the training dataset.
    """
    return pd.read_csv(DATASET_PATH)