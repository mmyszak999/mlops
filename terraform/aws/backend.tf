terraform {
  backend "s3" {
    bucket  = "mlops-backend-s3"
    key     = "mlops/terraform.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}