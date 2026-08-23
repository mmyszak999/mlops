resource "google_artifact_registry_repository" "mlops" {
  location      = var.region
  repository_id = "mlops-thesis-k8s"
  description   = "MLOps Kubernetes Docker images"
  format        = "DOCKER"

  depends_on = [
    google_project_service.required
  ]
}