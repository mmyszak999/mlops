import boto3
import json

runtime = boto3.client("sagemaker-runtime")

# Dane przykładowego pasażera:
# Pclass=3
# Age=22
# SibSp=1
# Parch=0
# Fare=7.25
# Sex=male
# Embarked=S

payload = [[
    3,      # Pclass
    22,     # Age
    1,      # SibSp
    0,      # Parch
    7.25,   # Fare
    0,      # Sex_female
    1,      # Sex_male
    0,      # Embarked_C
    0,      # Embarked_Q
    1       # Embarked_S
]]

response = runtime.invoke_endpoint(
    EndpointName="mlops-thesis-endpoint",
    ContentType="application/json",
    Body=json.dumps(payload)
)

result = response["Body"].read().decode()

print("Prediction:", result)