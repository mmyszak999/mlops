import boto3
import json

runtime = boto3.client(
    "sagemaker-runtime",
    region_name="us-east-1"
)

payload = [[
    1,        # Pclass
    12,       # Age
    0,        # SibSp
    0,        # Parch
    1311.2833,  # Fare
    1,        # Sex_female
    0,        # Sex_male
    0,        # Embarked_C
    1,        # Embarked_Q
    0         # Embarked_S
]]
"""
    3,
    45,
    0,
    0,
    7.25,
    0,
    1,
    0,
    0,
    1

    2,
    30,
    1,
    1,
    25,
    1,
    0,
    1,
    0,
    0


"""
response = runtime.invoke_endpoint(
    EndpointName="mlops-thesis-endpoint",
    ContentType="application/json",
    Body=json.dumps(payload)
)

print(response["Body"].read().decode())