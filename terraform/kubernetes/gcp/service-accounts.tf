resource "google_service_account" "gke_nodes" {
  account_id   = "mlops-gke-nodes"
  display_name = "MLOps GKE Nodes"
}

resource "google_service_account" "training" {
  account_id   = "mlops-gke-training"
  display_name = "MLOps GKE Training"
}

resource "google_service_account" "inference" {
  account_id   = "mlops-gke-inference"
  display_name = "MLOps GKE Inference"
}

resource "google_service_account" "mlflow" {
  account_id   = "mlops-gke-mlflow"
  display_name = "MLOps GKE MLflow"
}