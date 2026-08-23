resource "google_container_cluster" "gke" {
  name     = var.cluster_name
  location = var.zone

  network    = google_compute_network.gke.id
  subnetwork = google_compute_subnetwork.gke.id

  remove_default_node_pool = true
  initial_node_count       = 1

  deletion_protection = false

  networking_mode = "VPC_NATIVE"

  ip_allocation_policy {
    cluster_secondary_range_name  = "gke-pods"
    services_secondary_range_name = "gke-services"
  }

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  release_channel {
    channel = "REGULAR"
  }

  depends_on = [
    google_project_service.required
  ]
}


resource "google_container_node_pool" "main" {
  name       = "mlops-gke-node-pool"
  location   = var.zone
  cluster    = google_container_cluster.gke.name
  node_count = 1

  node_config {
    machine_type = var.node_machine_type

    disk_type    = "pd-balanced"
    disk_size_gb = 30

    image_type = "COS_CONTAINERD"

    service_account = google_service_account.gke_nodes.email

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    workload_metadata_config {
      mode = "GKE_METADATA"
    }

    labels = {
      environment = "thesis"
      workload    = "mlops"
    }
  }

  depends_on = [
    google_container_cluster.gke,
    google_project_iam_member.gke_node_logging,
    google_project_iam_member.gke_node_monitoring,
    google_artifact_registry_repository_iam_member.gke_node_reader
  ]
}