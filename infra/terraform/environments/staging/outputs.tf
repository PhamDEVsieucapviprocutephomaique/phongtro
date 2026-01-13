output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "eks_cluster_name" {
  description = "EKS cluster name"
  value       = module.eks.cluster_name
}

output "eks_cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = module.eks.cluster_endpoint
}

output "backend_ecr_url" {
  description = "Backend ECR repository URL"
  value       = module.ecr.backend_repository_url
}

output "frontend_ecr_url" {
  description = "Frontend ECR repository URL"
  value       = module.ecr.frontend_repository_url
}

output "configure_kubectl" {
  description = "Command to configure kubectl"
  value       = "aws eks update-kubeconfig --region ${var.aws_region} --name ${module.eks.cluster_name}"
}



# RDS Outputs
output "db_endpoint" {
  description = "RDS endpoint"
  value       = module.rds.db_instance_endpoint
}

output "db_address" {
  description = "RDS address"
  value       = module.rds.db_instance_address
}

output "db_name" {
  description = "Database name"
  value       = module.rds.db_name
}

output "db_password_secret_arn" {
  description = "Secret ARN for DB password"
  value       = module.rds.db_password_secret_arn
}

# S3 Outputs
output "s3_uploads_bucket" {
  description = "S3 uploads bucket name"
  value       = module.s3.uploads_bucket_name
}

output "s3_backups_bucket" {
  description = "S3 backups bucket name"
  value       = module.s3.backups_bucket_name
}