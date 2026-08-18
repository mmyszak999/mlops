from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def create_model() -> RandomForestClassifier:
    """
    Create the Random Forest model
    with fixed parameters used in the experiments.
    """

    return RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_split=5,
        random_state=42,
    )


def train_model(
    model: RandomForestClassifier,
    X_train,
    y_train,
):
    """
    Train the model.
    """

    model.fit(
        X_train,
        y_train,
    )

    return model


def evaluate_model(
    model: RandomForestClassifier,
    X_test,
    y_test,
) -> float:
    """
    Calculate model accuracy.
    """

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    return accuracy