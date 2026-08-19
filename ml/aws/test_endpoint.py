import boto3
import json


runtime = boto3.client(
    "sagemaker-runtime",
    region_name="us-east-1"
)


payload = {
    "Pclass": 1,
    "Sex": "female",
    "Age": 12,
    "SibSp": 0,
    "Parch": 0,
    "Fare": 1311.2833,
    "Embarked": "Q"
}


response = runtime.invoke_endpoint(
    EndpointName="mlops-thesis-endpoint",
    ContentType="application/json",
    Body=json.dumps(payload)
)


print(response["Body"].read().decode())