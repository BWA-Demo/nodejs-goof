# Demo Terraform for Snyk IaC scanning (nodejs-goof).
# Intentionally contains a few minor misconfigurations so `snyk iac test`
# has something to report. NOT for real deployment.

provider "aws" {
  region = "us-east-1"
}

# S3 bucket with no encryption / versioning / logging, and a public-read ACL.
resource "aws_s3_bucket" "data" {
  bucket = "nodejs-goof-demo-bucket"
}

resource "aws_s3_bucket_acl" "data" {
  bucket = aws_s3_bucket.data.id
  acl    = "public-read" # Snyk: S3 bucket is publicly readable
}

# Security group that exposes SSH to the entire internet.
resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "web server security group"

  ingress {
    description = "SSH from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Snyk: SSH open to 0.0.0.0/0
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
