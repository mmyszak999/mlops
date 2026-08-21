data "google_project" "current" {
  project_id = var.project_id
}

resource "google_project_service_identity" "vertex_ai" {
  project = var.project_id
  service = "aiplatform.googleapis.com"

  depends_on = [
    google_project_service.required["aiplatform.googleapis.com"]
  ]
}

resource "google_storage_bucket_iam_member" "vertex_ai_reader" {
  bucket = google_storage_bucket.models.name

  role = "roles/storage.objectViewer"

  member = google_project_service_identity.vertex_ai.member

  depends_on = [
    google_project_service_identity.vertex_ai
  ]
}