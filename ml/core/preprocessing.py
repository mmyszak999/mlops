import pandas as pd
from sklearn.model_selection import train_test_split


def preprocess_data(
    df: pd.DataFrame,
):
    """
    Prepare the Titanic dataset for model training.

    Returns:
        X_train
        X_test
        y_train
        y_test
        feature_columns
    """

    df = df.copy()

    # Fill missing values
    df["Age"] = df["Age"].fillna(
        df["Age"].median()
    )

    df["Embarked"] = df["Embarked"].fillna(
        df["Embarked"].mode()[0]
    )

    # Target
    y = df["Survived"]

    # Features
    X = df.drop(
        [
            "PassengerId",
            "Survived",
            "Name",
            "Ticket",
            "Cabin",
        ],
        axis=1,
    )

    # Encode categorical variables
    X = pd.get_dummies(X)

    feature_columns = X.columns.tolist()

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    return (
        X_train,
        X_test,
        y_train,
        y_test,
        feature_columns,
    )