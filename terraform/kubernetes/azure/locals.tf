locals {
  name_prefix = "mlops-thesis"

  storage_account_name = "mlopsak${random_string.suffix.result}"
  acr_name             = "mlopsaks${random_string.suffix.result}"

  training_identity_name  = "mlops-aks-training"
  inference_identity_name = "mlops-aks-inference"
  mlflow_identity_name    = "mlops-aks-mlflow"
}