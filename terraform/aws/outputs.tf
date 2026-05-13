output "bucket_name" {
  description = "S3 bucket name"
  value       = aws_s3_bucket.ml_bucket.bucket
}

output "sagemaker_role_arn" {
  description = "IAM role for SageMaker"
  value       = aws_iam_role.sagemaker_role.arn
}