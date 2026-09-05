terraform {
  backend "s3" {
    bucket         = "cloud-resume-tfstate-204284492976-xz1ghl"
    key            = "prod/terraform.tfstate"
    region         = "eu-north-1"
    dynamodb_table = "cloud-resume-tf-locks"
    encrypt        = true
  }
}
