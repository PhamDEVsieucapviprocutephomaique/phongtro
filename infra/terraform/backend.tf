terraform {
    backend s3 {
        bucket = "s3bucket1812learninfra01"
        key = "learninfra1/staging/terraform.tfstate"
        region = "ap-southeast-1"
        dynamodb_table = "terraform-state-lock"
        encrypt = true
    }
}