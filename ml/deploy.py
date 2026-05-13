import sagemaker
from sagemaker.sklearn.model import SKLearnModel

role = "YOUR_SAGEMAKER_ROLE_ARN"

session = sagemaker.Session()

model = SKLearnModel(
    model_data="file://model.pkl",
    role=role,
    framework_version="1.2-1",
    entry_point="predict.py"
)

predictor = model.deploy(
    initial_instance_count=1,
    instance_type="ml.t2.medium"
)

print("Endpoint deployed")