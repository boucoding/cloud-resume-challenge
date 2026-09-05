output "s3_bucket_name" {
  description = "S3 bucket for Terraform remote state"
  value       = aws_s3_bucket.terraform_state.id
}

output "dynamodb_table_name" {
  description = "DynamoDB table for Terraform state locking"
  value       = aws_dynamodb_table.terraform_locks.name
}

output "github_actions_role_arn" {
  description = "IAM Role ARN to configure in GitHub Secrets/Variables for OIDC"
  value       = aws_iam_role.github_actions_role.arn
}

output "aws_region" {
  description = "AWS Region configured"
  value       = var.aws_region
}
