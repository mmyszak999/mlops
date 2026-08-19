output "cluster_name" {
  value = aws_eks_cluster.k8s.name
}

output "cluster_endpoint" {
  value = aws_eks_cluster.k8s.endpoint
}

output "cluster_region" {
  value = var.aws_region
}

output "vpc_id" {
  value = aws_vpc.k8s.id
}

output "model_bucket_name" {
  value = aws_s3_bucket.models.bucket
}

output "train_ecr_repository_url" {
  value = aws_ecr_repository.train.repository_url
}

output "inference_ecr_repository_url" {
  value = aws_ecr_repository.inference.repository_url
}

output "inference_ecr_repository_name" {
  value = aws_ecr_repository.inference.name
}

output "train_ecr_repository_name" {
  value = aws_ecr_repository.train.name
}

output "configure_kubectl_command" {
  value = "aws eks update-kubeconfig --region ${var.aws_region} --name ${aws_eks_cluster.k8s.name}"
}

output "mlflow_ecr_repository_name" {
  value = aws_ecr_repository.mlflow.name
}

output "mlflow_ecr_repository_url" {
  value = aws_ecr_repository.mlflow.repository_url
}