resource "google_compute_network" "gke" {
  name                    = "mlops-thesis-gke-vpc"
  auto_create_subnetworks = false

  depends_on = [
    google_project_service.required
  ]
}

resource "google_compute_subnetwork" "gke" {
  name          = "mlops-thesis-gke-subnet"
  ip_cidr_range = "10.20.0.0/20"
  region        = var.region
  network       = google_compute_network.gke.id

  private_ip_google_access = true

  secondary_ip_range {
    range_name    = "gke-pods"
    ip_cidr_range = "10.24.0.0/14"
  }

  secondary_ip_range {
    range_name    = "gke-services"
    ip_cidr_range = "10.28.0.0/20"
  }
}