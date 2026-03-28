output "api_gateway_url" {
    description = "Base API URL"
    value       = aws_apigatewayv2_stage.prod.invoke_url
}

output "api_endpoint" {
    description = "Available Endpoints"
    value = {
        ping    = "${aws_apigatewayv2_stage.prod.invoke_url}/ping"
        predict = "${aws_apigatewayv2_stage.prod.invoke_url}/predict"
    }
}

output "ecr_repository_url" {
    description = "ECR repo URL for Docker images to live"
    value       = aws_ecr_repository.housing_model.repository_url
}

output "lambda_function_name" {
    description = "Name for lambda function"
    value       = aws_lambda_function.ml_api.function_name
}

output "gha_role_arn" {
    description = "IAM role ARN for GitHub Actions OIDC — paste into deploy.yml"
    value       = aws_iam_role.github_actions.arn
}
