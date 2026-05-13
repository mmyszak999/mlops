import boto3

sm = boto3.client(
    "sagemaker",
    region_name="us-east-1"
)

endpoint_name = "mlops-thesis-endpoint"

try:
    sm.delete_endpoint(
        EndpointName=endpoint_name
    )

    print("Endpoint deleted")

except Exception as e:
    print(f"Endpoint delete error: {e}")

try:
    sm.delete_endpoint_config(
        EndpointConfigName=endpoint_name
    )

    print("Endpoint config deleted")

except Exception as e:
    print(f"Endpoint config delete error: {e}")

models = sm.list_models(
    NameContains="sagemaker-scikit"
)

for model in models["Models"]:

    try:
        sm.delete_model(
            ModelName=model["ModelName"]
        )

        print(f"Deleted model: {model['ModelName']}")

    except Exception as e:
        print(e)