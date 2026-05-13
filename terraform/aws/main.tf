
resource "random_id" "suffix" {
  byte_length = 4
}
/*
# S3 bucket
resource "aws_s3_bucket" "ml_bucket" {
  bucket = "mlops-thesis-${random_id.suffix.hex}"

  tags = {
    Project = "mlops-thesis"
  }
}

# CloudWatch logs
resource "aws_cloudwatch_log_group" "logs" {
  name              = "/aws/sagemaker/mlops-thesis-${random_id.suffix.hex}"
  retention_in_days = 7
}

*/