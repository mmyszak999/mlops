resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "google_storage_bucket" "models" {
  name = "${var.project_name}-${random_id.bucket_suffix.hex}"

  location = var.region

  uniform_bucket_level_access = true

  force_destroy = true

  depends_on = [
    google_project_service.required
  ]
}