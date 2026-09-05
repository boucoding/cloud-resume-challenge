terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "CloudResumeChallenge"
      Owner       = "Abdelrahman Ahmed"
      ManagedBy   = "Terraform"
      Environment = var.environment
    }
  }
}

# Secondary provider for ACM Certificate in us-east-1 required by CloudFront
provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"

  default_tags {
    tags = {
      Project     = "CloudResumeChallenge"
      Owner       = "Abdelrahman Ahmed"
      ManagedBy   = "Terraform"
      Environment = var.environment
    }
  }
}

data "aws_caller_identity" "current" {}
