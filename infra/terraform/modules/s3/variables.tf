variable "environment" {
  description = "Environment name"
  type        = string
}

variable "bucket_name" {
  description = "Base bucket name"
  type        = string
  default     = "phongtro-app"
}

variable "enable_versioning" {
  description = "Enable S3 versioning"
  type        = bool
  default     = true
}

variable "allowed_origins" {
  description = "Allowed CORS origins"
  type        = list(string)
  default     = ["*"]  # Trong production, chỉ định domain cụ thể
}