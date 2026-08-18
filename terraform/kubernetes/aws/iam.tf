# =========================================================
# EKS CLUSTER ROLE
# =========================================================

resource "aws_iam_role" "eks_cluster" {
  name = "${var.project_name}-cluster-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "eks.amazonaws.com"
        }

        Action = [
          "sts:AssumeRole",
          "sts:TagSession"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  role = aws_iam_role.eks_cluster.name

  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}


# =========================================================
# EKS NODE ROLE
# =========================================================

resource "aws_iam_role" "eks_node" {
  name = "${var.project_name}-node-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "ec2.amazonaws.com"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "eks_node_worker_policy" {
  role = aws_iam_role.eks_node.name

  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
}

resource "aws_iam_role_policy_attachment" "eks_node_ecr_policy" {
  role = aws_iam_role.eks_node.name

  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPullOnly"
}

resource "aws_iam_role_policy_attachment" "eks_node_cni_policy" {
  role = aws_iam_role.eks_node.name

  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
}


# =========================================================
# TRAINING POD ROLE
# =========================================================

resource "aws_iam_role" "training_pod" {
  name = "${var.project_name}-training-pod-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "pods.eks.amazonaws.com"
        }

        Action = [
          "sts:AssumeRole",
          "sts:TagSession"
        ]
      }
    ]
  })
}


# =========================================================
# INFERENCE POD ROLE
# =========================================================

resource "aws_iam_role" "inference_pod" {
  name = "${var.project_name}-inference-pod-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "pods.eks.amazonaws.com"
        }

        Action = [
          "sts:AssumeRole",
          "sts:TagSession"
        ]
      }
    ]
  })
}

# =========================================================
# TRAINING POD IDENTITY
# =========================================================

resource "aws_eks_pod_identity_association" "training" {
  cluster_name    = aws_eks_cluster.k8s.name
  namespace       = "mlops"
  service_account = "mlops-training"
  role_arn        = aws_iam_role.training_pod.arn

  depends_on = [
    aws_eks_addon.pod_identity_agent
  ]
}


# =========================================================
# INFERENCE POD IDENTITY
# =========================================================

resource "aws_eks_pod_identity_association" "inference" {
  cluster_name    = aws_eks_cluster.k8s.name
  namespace       = "mlops"
  service_account = "mlops-inference"
  role_arn        = aws_iam_role.inference_pod.arn

  depends_on = [
    aws_eks_addon.pod_identity_agent
  ]
}

# =========================================================
# MLFLOW POD ROLE
# =========================================================

resource "aws_iam_role" "mlflow_pod" {
  name = "${var.project_name}-mlflow-pod-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          Service = "pods.eks.amazonaws.com"
        }

        Action = [
          "sts:AssumeRole",
          "sts:TagSession"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy" "mlflow_s3" {
  name = "${var.project_name}-mlflow-s3"
  

  role = aws_iam_role.mlflow_pod.id

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket",
          "s3:AbortMultipartUpload"
        ]

        Resource = [
          aws_s3_bucket.models.arn,
          "${aws_s3_bucket.models.arn}/*"
        ]
      }
    ]
  })
}

resource "aws_eks_pod_identity_association" "mlflow" {
  cluster_name    = aws_eks_cluster.k8s.name
  namespace       = "mlops"
  service_account = "mlflow"
  role_arn        = aws_iam_role.mlflow_pod.arn

  depends_on = [
    aws_eks_addon.pod_identity_agent
  ]
}