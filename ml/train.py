import tarfile

import boto3
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

df = pd.read_csv("data/data.csv")

df = df.dropna()

y = df["Survived"]

X = df.drop(
    [
        "Survived",
        "Name",
        "Ticket",
        "Cabin"
    ],
    axis=1
)

X = pd.get_dummies(X)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

preds = model.predict(X_test)

accuracy = accuracy_score(y_test, preds)

print(f"Model accuracy: {accuracy}")

joblib.dump(model, "model.pkl")

with tarfile.open("model.tar.gz", "w:gz") as tar:
    tar.add("model.pkl")

bucket_name = "mlops-thesis-d37b3fa3"

s3 = boto3.client("s3")

s3.upload_file(
    "model.tar.gz",
    bucket_name,
    "models/model.tar.gz"
)

print("Model uploaded to S3")