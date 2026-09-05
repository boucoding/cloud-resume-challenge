variable "aws_region" {
  type        = string
  description = "AWS region for bootstrap state and resources"
  default     = "eu-north-1"
}

variable "state_bucket_prefix" {
  type        = string
  description = "Prefix for Terraform state S3 bucket"
  default     = "cloud-resume-tfstate"
}

variable "lock_table_name" {
  type        = string
  description = "DynamoDB table name for Terraform state locking"
  default     = "cloud-resume-tf-locks"
}

variable "github_repo" {
  type        = string
  description = "GitHub repository formatted as 'owner/repo' (e.g. boucoding/cloud-resume-challenge)"
  default     = "boucoding/cloud-resume-challenge"
}
