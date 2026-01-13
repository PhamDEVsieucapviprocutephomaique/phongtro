output "uploads_bucket_id" {
  description = "Uploads bucket ID"
  value       = aws_s3_bucket.uploads.id
}

output "uploads_bucket_arn" {
  description = "Uploads bucket ARN"
  value       = aws_s3_bucket.uploads.arn
}

output "uploads_bucket_name" {
  description = "Uploads bucket name"
  value       = aws_s3_bucket.uploads.bucket
}

output "backups_bucket_id" {
  description = "Backups bucket ID"
  value       = aws_s3_bucket.backups.id
}

output "backups_bucket_arn" {
  description = "Backups bucket ARN"
  value       = aws_s3_bucket.backups.arn
}

output "backups_bucket_name" {
  description = "Backups bucket name"
  value       = aws_s3_bucket.backups.bucket
}

output "s3_access_policy_arn" {
  description = "IAM policy ARN for S3 access"
  value       = aws_iam_policy.s3_access.arn
}