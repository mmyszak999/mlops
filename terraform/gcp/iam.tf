resource "google_storage_bucket_iam_member" "vertex_ai_reader" {
  bucket = google_storage_bucket.models.name

  role = "roles/storage.objectViewer"

  member = "serviceAccount:service-${data.google_project.current.number}@gcp-sa-aiplatform.iam.gserviceaccount.com"

  depends_on = [
    google_project_service.required
  ]
}

data "google_project" "current" {
  project_id = var.project_id
}