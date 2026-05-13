resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "ml_bucket" {
  bucket = "mlops-thesis-${random_id.suffix.hex}"

  tags = {
    Project = "mlops-thesis"
  }
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.ml_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_cloudwatch_log_group" "sagemaker_logs" {
  name              = "/aws/sagemaker/mlops-thesis"
  retention_in_days = 7
}