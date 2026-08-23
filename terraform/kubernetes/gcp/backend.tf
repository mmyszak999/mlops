terraform {
  backend "gcs" {
    bucket = "mlops-backend-s3"
    prefix = "gcp/kubernetes"
  }
}