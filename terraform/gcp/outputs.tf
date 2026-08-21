output "project_id" {
  value = var.project_id
}

output "region" {
  value = var.region
}

output "model_bucket_name" {
  value = google_storage_bucket.models.name
}

output "model_bucket_uri" {
  value = "gs://${google_storage_bucket.models.name}"
}

output "artifact_registry_repository" {
  value = google_artifact_registry_repository.mlops.name
}

output "artifact_registry_repository_url" {
  value = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.mlops.repository_id}"
}