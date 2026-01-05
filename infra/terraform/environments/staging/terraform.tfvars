# Thay đổi các giá trị này theo nhu cầu
aws_region         = "ap-southeast-1"
environment        = "staging"
cluster_name       = "my-app-staging-eks"
kubernetes_version = "1.28"

# Network
vpc_cidr             = "10.0.0.0/16"
public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24"]
private_subnet_cidrs = ["10.0.11.0/24", "10.0.12.0/24"]
availability_zones   = ["ap-southeast-1a", "ap-southeast-1b"]

# EKS Node Group
desired_size   = 2
max_size       = 3
min_size       = 1
instance_types = ["t3.medium"]