variable "gcp_svc_key" {
}

variable "gcp_project_id" {
}

variable "gcp_region" {
}

variable "github_repo" {
}

variable "fqdn" {
  description = "The fully qualified domain name of the system we are setting up"
  default     = "dev.freeworldcertified.org"
}

variable "postgres_database" {
  description = "The postgres database name"
  default     = "pg-database"
}

variable "postgres_user" {
  description = "The postgres username"
  default     = "pguser"
}

variable "gcp_service_list" {
  description = "The list of apis necessary for the project"
  type        = list(string)
  default = [
    "cloudresourcemanager.googleapis.com",
    "iam.googleapis.com",
    "sqladmin.googleapis.com",
    "secretmanager.googleapis.com",
    "cloudbuild.googleapis.com",
    "run.googleapis.com",
    "artifactregistry.googleapis.com",
    "compute.googleapis.com",
    "clouddeploy.googleapis.com",
  ]
}
