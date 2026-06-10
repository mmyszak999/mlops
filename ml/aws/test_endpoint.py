import boto3
import json

runtime = boto3.client(
    "sagemaker-runtime",
    region_name="us-east-1"
)

payload = [[
    1,        # Pclass
    38,       # Age
    1,        # SibSp
    0,        # Parch
    71.2833,  # Fare
    1,        # Sex_female
    0,        # Sex_male
    1,        # Embarked_C
    0,        # Embarked_Q
    0         # Embarked_S
]]

response = runtime.invoke_endpoint(
    EndpointName="mlops-thesis-endpoint",
    ContentType="application/json",
    Body=json.dumps(payload)
)

print(response["Body"].read().decode())