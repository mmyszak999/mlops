resource "google_artifact_registry_repository_iam_member" "gke_node_reader" {
  project    = var.project_id
  location   = google_artifact_registry_repository.mlops.location
  repository = google_artifact_registry_repository.mlops.repository_id

  role = "roles/artifactregistry.reader"

  member = "serviceAccount:${google_service_account.gke_nodes.email}"
}

resource "google_project_iam_member" "gke_node_logging" {
  project = var.project_id

  role = "roles/logging.logWriter"

  member = "serviceAccount:${google_service_account.gke_nodes.email}"
}

resource "google_project_iam_member" "gke_node_monitoring" {
  project = var.project_id

  role = "roles/monitoring.metricWriter"

  member = "serviceAccount:${google_service_account.gke_nodes.email}"
}

resource "google_storage_bucket_iam_member" "mlflow_bucket" {
  bucket = google_storage_bucket.models.name

  role = "roles/storage.objectAdmin"

  member = "serviceAccount:${google_service_account.mlflow.email}"
}

resource "google_storage_bucket_iam_member" "mlflow_bucket_viewer" {
  bucket = google_storage_bucket.models.name

  role = "roles/storage.bucketViewer"

  member = "serviceAccount:${google_service_account.mlflow.email}"
}

resource "google_storage_bucket_iam_member" "training_bucket" {
  bucket = google_storage_bucket.models.name

  role = "roles/storage.objectAdmin"

  member = "serviceAccount:${google_service_account.training.email}"
}

resource "google_storage_bucket_iam_member" "inference_bucket" {
  bucket = google_storage_bucket.models.name

  role = "roles/storage.objectViewer"

  member = "serviceAccount:${google_service_account.inference.email}"
}

data "google_project" "current" {
  project_id = var.project_id
}

resource "google_service_account_iam_member" "training_workload_identity" {
  service_account_id = google_service_account.training.name

  role = "roles/iam.workloadIdentityUser"

  member = "principal://iam.googleapis.com/projects/${data.google_project.current.number}/locations/global/workloadIdentityPools/${var.project_id}.svc.id.goog/subject/ns/mlops/sa/mlops-training"
}

resource "google_service_account_iam_member" "inference_workload_identity" {
  service_account_id = google_service_account.inference.name

  role = "roles/iam.workloadIdentityUser"

  member = "principal://iam.googleapis.com/projects/${data.google_project.current.number}/locations/global/workloadIdentityPools/${var.project_id}.svc.id.goog/subject/ns/mlops/sa/mlops-inference"
}

resource "google_service_account_iam_member" "mlflow_workload_identity" {
  service_account_id = google_service_account.mlflow.name

  role = "roles/iam.workloadIdentityUser"

  member = "principal://iam.googleapis.com/projects/${data.google_project.current.number}/locations/global/workloadIdentityPools/${var.project_id}.svc.id.goog/subject/ns/mlops/sa/mlflow"
}