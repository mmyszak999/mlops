import sagemaker

from sagemaker.sklearn.model import SKLearnModel

role = "arn:aws:iam::154959838069:role/sagemaker-execution-role-d37b3fa3"

bucket = "mlops-thesis-d37b3fa3"

session = sagemaker.Session()

model = SKLearnModel(
    model_data=f"s3://{bucket}/models/model.tar.gz",
    role=role,
    framework_version="1.2-1",
    entry_point="predict.py",
    sagemaker_session=session
)

predictor = model.deploy(
    endpoint_name="mlops-thesis-endpoint",
    initial_instance_count=1,
    instance_type="ml.t2.medium"
)

print("Endpoint deployed")