variable "aws_region" {
    description = "AWS region - defaults to cheapest"
    type        = string
    default     = "us-east-1"
}

variable "project_name" {
    description = "Name of repo project"
    type        = string
    default     = "ml-model-deployment"
}

variable "environment" {
    description = "Environment name (we only use prod for AWS)"
    type        = string
    default     = "prod"
}

variable "lambda_memory_size" {
    description = "Memory for Lambda"
    type        = number
    default     = 2048
}

variable "lambda_timeout" {
    description = "Number of seconds before lambda timeout"
    type        = number
    default     = 30
}

variable "ecr_image_tag" {
    description = "Docker image tag to deploy"
    type        = string
    default     = "latest"
}
