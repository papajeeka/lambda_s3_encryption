locals {
  lambda_zip_location = "output/david_nassy.zip"
}

data "archive_file" "david_nassy" {
  type        = "zip"
  source_file = "main.py"
  output_path = local.lambda_zip_location
}

resource "aws_iam_role" "s3_encryption_remediation-role-tbh4er8h_role" {
  name = "davidnassy_lambda_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_lambda_function" "david_lambda" {
  # If the file is not in the current working directory you will need to include a 
  # path.module in the filename.
  filename      = local.lambda_zip_location
  function_name = "lambda_function_david"
  role          = aws_iam_role.s3_encryption_remediation-role-tbh4er8h_role.arn
  handler       = "main.lambda_handler"

  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # source_code_hash = "${base64sha256(file("lambda_function_payload.zip"))}"
  #   terrsource_code_hash = filebase64sha256("lambda_function_payload.zip")

  runtime = "python3.8"

  environment {
    variables = {
      foo = "bar"
    }
  }
}

resource "aws_iam_policy" "nassylambda_policy" {
  name        = "noel_lambda-policy"
  description = "A test policy"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": "arn:aws:s3:::*"
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "collins-attach" {
  role       = aws_iam_role.s3_encryption_remediation-role-tbh4er8h_role.name
  policy_arn = aws_iam_policy.nassylambda_policy.arn
}
