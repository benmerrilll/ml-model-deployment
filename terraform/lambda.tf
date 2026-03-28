resource "aws_lambda_function" "ml_api" {
    function_name = "ml-housing-prediction"
    role          = aws_iam_role.lambda_role.arn
    package_type  = "Image"
    image_uri     = "${aws_ecr_repository.housing_model.repository_url}:v1"

    architectures = ["x86_64"]

    memory_size   = var.lambda_memory_size
    timeout       = var.lambda_timeout

    environment {
        variables = {
            LOG_LEVEL   = "INFO"
            ENVIRONMENT = "production"
            DEPLOYED_AT = "2026-03-27"
        }
    }

    depends_on = [aws_ecr_repository.housing_model]
}
