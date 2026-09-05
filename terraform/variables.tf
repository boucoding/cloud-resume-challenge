variable "aws_region" {
  type        = string
  description = "AWS deployment region"
  default     = "eu-north-1"
}

variable "environment" {
  type        = string
  description = "Deployment environment"
  default     = "prod"
}

variable "project_name" {
  type        = string
  description = "Project name prefix for resources"
  default     = "cloud-resume"
}

# Custom Domain Toggle & Settings
variable "enable_custom_domain" {
  type        = bool
  description = "Set to true if you own a custom domain and want Route 53 + ACM SSL integration"
  default     = false
}

variable "domain_name" {
  type        = string
  description = "Custom domain name (e.g. resume.yourname.com or yourname.com)"
  default     = ""
}
