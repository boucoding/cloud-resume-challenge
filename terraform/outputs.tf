output "s3_bucket_id" {
  description = "Name of the S3 static website bucket"
  value       = aws_s3_bucket.frontend.id
}

output "cloudfront_distribution_id" {
  description = "ID of CloudFront distribution for cache invalidations"
  value       = aws_cloudfront_distribution.resume_cdn.id
}

output "cloudfront_domain_name" {
  description = "Default CloudFront domain URL"
  value       = "https://${aws_cloudfront_distribution.resume_cdn.domain_name}"
}

output "custom_domain_url" {
  description = "Custom domain URL if enabled"
  value       = var.enable_custom_domain ? "https://${var.domain_name}" : "Custom domain disabled"
}

output "api_gateway_url" {
  description = "Invoke URL for API Gateway HTTP API"
  value       = aws_apigatewayv2_stage.default_stage.invoke_url
}

output "visitor_endpoint" {
  description = "Full URL to visitor counter endpoint"
  value       = "${aws_apigatewayv2_stage.default_stage.invoke_url}visitors"
}

output "lambda_function_name" {
  description = "Name of the visitor counter Lambda function"
  value       = aws_lambda_function.visitor_counter.function_name
}
