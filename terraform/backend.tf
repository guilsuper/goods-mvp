# https://cloud.google.com/docs/terraform/resource-management/store-state

# this stores the terraform state files in a gcp bucket; the actual
# bucket name must be used here
terraform {
  backend "gcs" {
    bucket = "7d5b5162014d7086-bucket-tfstate"
    prefix = "terraform/state"
  }
}
