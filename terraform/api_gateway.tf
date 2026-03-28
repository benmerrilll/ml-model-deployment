resource "aws_apigatewayv2_api" "ml_api" {
    name          = "${var.project_name}-api"
    protocol_type = "HTTP"

    description = "ML Housing Price Prediction API"
}

resource "aws_apigatewayv2_integration" "lambda" {
    api_id           = aws_apigatewayv2_api.ml_api.id
    integration_type = "AWS_PROXY"
    integration_uri  = aws_lambda_function.ml_api.invoke_arn
}

resource "aws_apigatewayv2_route" "ping" {
    api_id    = aws_apigatewayv2_api.ml_api.id
    route_key = "GET /ping"
    target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_apigatewayv2_route" "predict" {
    api_id    = aws_apigatewayv2_api.ml_api.id
    route_key = "POST /predict"
    target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_apigatewayv2_stage" "prod" {
    api_id      = aws_apigatewayv2_api.ml_api.id
    name        = "$default"
    auto_deploy = true
}

resource "aws_lambda_permission" "api_gateway" {
    statement_id  = "AllowAPIGatewayInvoke"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.ml_api.function_name
    principal     = "apigateway.amazonaws.com"
    source_arn    = "${aws_apigatewayv2_api.ml_api.execution_arn}/*/*"
}
