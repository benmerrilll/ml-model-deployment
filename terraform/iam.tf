resource "aws_iam_openid_connect_provider" "github" {
    url             = "https://token.actions.githubusercontent.com"
    client_id_list  = ["sts.amazonaws.com"]
    thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
}

resource "aws_iam_role" "lambda_role" {
    name = "${var.project_name}-lambda-role"

    assume_role_policy = jsonencode({
        Version   = "2012-10-17"
        Statement = [{
            Action = "sts:AssumeRole"
            Effect = "Allow"
            Principal = {
                Service = "lambda.amazonaws.com"
            }
        }]
    })
}

resource "aws_iam_role" "github_actions" {
    name = "${var.project_name}-gha-role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [{
            Effect    = "Allow"
            Action    = "sts:AssumeRoleWithWebIdentity"
            Principal = {
                Federated = aws_iam_openid_connect_provider.github.arn
            }
            Condition = {
                StringEquals = {
                    "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
                    "token.actions.githubusercontent.com:sub" = "repo:benmerrilll/ml-model-deployment:ref:refs/heads/main"
                }
            }
        }]
    })
}

resource "aws_iam_role_policy" "github_actions_deploy" {
    name = "${var.project_name}-gha-deploy-policy"
    role = aws_iam_role.github_actions.id

    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                # ECR login (account-level, cannot be scoped to a resource)
                Sid      = "ECRAuth"
                Effect   = "Allow"
                Action   = "ecr:GetAuthorizationToken"
                Resource = "*"
            },
            {
                # ECR image push + Terraform ECR management
                Sid    = "ECRRepository"
                Effect = "Allow"
                Action = [
                    "ecr:BatchCheckLayerAvailability",
                    "ecr:InitiateLayerUpload",
                    "ecr:UploadLayerPart",
                    "ecr:CompleteLayerUpload",
                    "ecr:PutImage",
                    "ecr:CreateRepository",
                    "ecr:DescribeRepositories",
                    "ecr:DeleteRepository"
                ]
                Resource = "arn:aws:ecr:${var.aws_region}:*:repository/${var.project_name}"
            },
            {
                # Lambda deploy + Terraform Lambda management
                Sid    = "Lambda"
                Effect = "Allow"
                Action = [
                    "lambda:UpdateFunctionCode",
                    "lambda:GetFunction",
                    "lambda:CreateFunction",
                    "lambda:DeleteFunction",
                    "lambda:UpdateFunctionConfiguration",
                    "lambda:GetFunctionConfiguration",
                    "lambda:AddPermission",
                    "lambda:RemovePermission"
                ]
                Resource = "arn:aws:lambda:${var.aws_region}:*:function:ml-housing-prediction"
            },
            {
                # IAM — Terraform needs to manage the Lambda execution role
                Sid    = "IAM"
                Effect = "Allow"
                Action = [
                    "iam:GetRole",
                    "iam:CreateRole",
                    "iam:DeleteRole",
                    "iam:AttachRolePolicy",
                    "iam:DetachRolePolicy",
                    "iam:PassRole",
                    "iam:ListRolePolicies",
                    "iam:ListAttachedRolePolicies",
                    "iam:GetOpenIDConnectProvider",
                    "iam:CreateOpenIDConnectProvider",
                    "iam:DeleteOpenIDConnectProvider",
                    "iam:TagOpenIDConnectProvider"
                ]
                Resource = "*"
            },
            {
                # API Gateway — Terraform manages the HTTP API, routes, integrations, stage
                Sid      = "APIGateway"
                Effect   = "Allow"
                Action   = "apigateway:*"
                Resource = "arn:aws:apigateway:${var.aws_region}::*"
            }
        ]
    })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
    role       = aws_iam_role.lambda_role.name
    policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
