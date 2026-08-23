output "cluster_name" {
  value = google_container_cluster.gke.name
}

output "cluster_zone" {
  value = var.zone
}

output "cluster_region" {
  value = var.region
}

output "model_bucket_name" {
  value = google_storage_bucket.models.name
}

output "model_bucket_uri" {
  value = "gs://${google_storage_bucket.models.name}"
}

output "artifact_registry_repository_name" {
  value = google_artifact_registry_repository.mlops.repository_id
}

output "artifact_registry_repository_url" {
  value = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.mlops.repository_id}"
}

output "training_service_account_email" {
  value = google_service_account.training.email
}

output "inference_service_account_email" {
  value = google_service_account.inference.email
}

output "mlflow_service_account_email" {
  value = google_service_account.mlflow.email
}

output "gke_node_service_account_email" {
  value = google_service_account.gke_nodes.email
}

output "network_name" {
  value = google_compute_network.gke.name
}

output "subnetwork_name" {
  value = google_compute_subnetwork.gke.name
}