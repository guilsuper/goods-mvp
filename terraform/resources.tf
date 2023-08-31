#########################################################################################################################
# enable apis that this projects needs
resource "google_project_service" "gcp_services" {
  for_each = toset(var.gcp_service_list)
  project  = var.gcp_project_id
  service  = each.key
}


#########################################################################################################################
# https://cloud.google.com/load-balancing/docs/l7-internal/setting-up-l7-internal-serverless#gcloud_2
# https://cloud.google.com/blog/topics/developers-practitioners/new-terraform-module-serverless-load-balancing
# https://cloud.google.com/blog/topics/developers-practitioners/serverless-load-balancing-terraform-hard-way
# https://cloud.google.com/load-balancing/docs/https/setup-global-ext-https-serverless
# https://engineering.premise.com/tutorial-managing-serverless-gcp-load-balancers-dynamically-with-terraform-e15751853312

#########################################################################################################################
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_network
# https://cloud.google.com/vpc/docs/vpc


# global ip address for website (ie the load balancer)
resource "google_compute_global_address" "external_ip_address" {
  name         = "external-ip-address"
  ip_version   = "IPV4"
  address_type = "EXTERNAL"
}

# ssl certificate for the load balancer
resource "google_compute_managed_ssl_certificate" "lb_ssl_cert" {
  provider = google-beta
  name     = "dev-ssl-cert"

  managed {
    domains = [var.fqdn]
  }
}

# https load balancer
resource "google_compute_target_https_proxy" "https_proxy" {
  name    = "https-proxy"
  url_map = google_compute_url_map.url_map.id
  ssl_certificates = [
    google_compute_managed_ssl_certificate.lb_ssl_cert.name
  ]
  depends_on = [
    google_compute_managed_ssl_certificate.lb_ssl_cert
  ]
}

# http proxy (only used for redirect to the https site)
resource "google_compute_target_http_proxy" "http_proxy" {
  name    = "http-proxy"
  url_map = google_compute_url_map.http_redirect.id
}


# https://registry.terraform.io/providers/hashicorp/google/3.0.0-beta.1/docs/resources/compute_url_map
# url which maps various / to buckets and /api to backend
resource "google_compute_url_map" "url_map" {
  name            = "url-map"
  default_service = google_compute_backend_bucket.static_site.self_link

  host_rule {
    hosts        = ["*"]
    path_matcher = "allpaths"
  }
  path_matcher {
    name            = "allpaths"
    default_service = google_compute_backend_bucket.static_site.self_link

    path_rule {
      paths   = ["/api/*"]
      service = google_compute_backend_service.backend_service.self_link
    }
  }
}

# https://stackoverflow.com/questions/64375885/google-cloud-forwarding-rule-http-https-using-terraform
# redirect http to https
resource "google_compute_url_map" "http_redirect" {
  name = "http-redirect"

  default_url_redirect {
    redirect_response_code = "MOVED_PERMANENTLY_DEFAULT" # 301 redirect
    strip_query            = false
    https_redirect         = true
  }
}

# forward port 80 to the load balancer
resource "google_compute_global_forwarding_rule" "global_forwarding_rule" {
  name = "lb"

  target     = google_compute_target_http_proxy.http_proxy.id
  port_range = 80
  ip_address = google_compute_global_address.external_ip_address.address
}

# forward port 443 to the load balancer
resource "google_compute_global_forwarding_rule" "global_forwarding_rule_https" {
  name = "lb-https"

  target     = google_compute_target_https_proxy.https_proxy.id
  port_range = 443
  ip_address = google_compute_global_address.external_ip_address.address
}



#########################################################################################################################
# create github actions service account
resource "google_service_account" "github_actions_service_account" {
  account_id   = "github-actions-service-account"
  display_name = "GitHub Actions Service Account"
  description  = "Service Account for GitHub actions push builds into GCP to run ${var.fqdn}"
}

#########################################################################################################################
# create github workload identity pool
resource "google_iam_workload_identity_pool" "github_workload_identity_pool" {
  workload_identity_pool_id = "github-workload-identity-pool"
  display_name              = "GitHub Workload Identity Pool"
  description               = "Identity Pool GitHub Actions"
  disabled                  = false
}

# create github workload identify pool provider
resource "google_iam_workload_identity_pool_provider" "github_workload_identity_pool_provider" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.github_workload_identity_pool.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-wip-provider"
  display_name                       = "GitHub WIP Provider"
  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.repository" = "assertion.repository"
  }
  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

# allow authentications from the workload identity provider originating from your repository to impersonate the service account
resource "google_service_account_iam_binding" "github_actions_service_account_iam_binding" {
  service_account_id = google_service_account.github_actions_service_account.name

  role = "roles/iam.workloadIdentityUser"

  members = [
    "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github_workload_identity_pool.name}/attribute.repository/${var.github_repo}"
  ]
}

#########################################################################################################################
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/sql_database_instance
# https://cloud.google.com/sql/docs/postgres/instance-settings
resource "google_sql_database_instance" "postgres_main" {
  name             = "postgres-main-instance"
  database_version = "POSTGRES_15"

  settings {
    # This is NOT appropriate for production!
    tier      = "db-f1-micro"
    disk_size = "10" # gig

    # Enable this in production!
    # backup_configuration {
    #  enabled = true
    # }
    # ip_configuration {
    #  ipv4_enabled    = true
    #  private_network = "projects/${var.gcp_project_id}/global/networks/default"
    # }
  }
  deletion_protection = "true"
}

# create the database itself; inside of the instance
resource "google_sql_database" "postgres_database" {
  name     = var.postgres_database
  instance = google_sql_database_instance.postgres_main.name
}

# https://cloud.google.com/sql/docs/postgres/create-manage-users#terraform
# create postgres password
resource "random_password" "postgres_password" {
  length  = 24
  special = false
}

# create postgres user
resource "google_sql_user" "postgres_user" {
  name     = var.postgres_user
  instance = google_sql_database_instance.postgres_main.name
  password = random_password.postgres_password.result
}


#########################################################################################################################
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "google_storage_bucket_static_site" {
  name     = "fwc-static-site"
  location = var.gcp_region

  storage_class = "STANDARD"
  force_destroy = true

  uniform_bucket_level_access = true

  website {
    main_page_suffix = "index.html"
    not_found_page   = "index.html"
  }
  cors {
    origin          = ["https://${var.fqdn}"]
    method          = ["GET", "HEAD", ] # "PUT", "POST", "DELETE"
    response_header = ["*"]
    max_age_seconds = 60
  }
}

# grant read access to allUsers (ie the internet)
resource "google_storage_bucket_iam_member" "member" {
  bucket = google_storage_bucket.google_storage_bucket_static_site.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}

# this is what connects the load balancer to the buckets static content
resource "google_compute_backend_bucket" "static_site" {
  name        = "fwc-static-site"
  description = "Contains static resources for app"
  bucket_name = google_storage_bucket.google_storage_bucket_static_site.name
  enable_cdn  = false
}

#########################################################################################################################
# create django secret key
resource "random_password" "django_secret_key" {
  length  = 24
  special = false
}

resource "google_secret_manager_secret" "secret_django_secret_key" {
  secret_id = "django-secret-key"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "secret_django_secret_key_version" {
  secret      = google_secret_manager_secret.secret_django_secret_key.id
  secret_data = random_password.django_secret_key.result
}

# allow cloud run & cloud build service to access secret
resource "google_secret_manager_secret_iam_binding" "django_secret_key_account_bindings" {
  project   = google_secret_manager_secret.secret_django_secret_key.project
  secret_id = google_secret_manager_secret.secret_django_secret_key.secret_id
  role      = "roles/secretmanager.secretAccessor"
  members = [
    "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com",
    "serviceAccount:${data.google_project.project.number}@cloudbuild.gserviceaccount.com"
  ]
}

# secret place to store the secret key
resource "google_secret_manager_secret" "secret_django_database_url" {
  secret_id = "django-database-url"
  replication {
    automatic = true
  }
}

# the specific version of the secret with its content
resource "google_secret_manager_secret_version" "secret_django_database_url_version" {
  secret      = google_secret_manager_secret.secret_django_database_url.id
  secret_data = "postgres://${var.postgres_user}:${random_password.postgres_password.result}@//cloudsql/${var.gcp_project_id}:${var.gcp_region}:${google_sql_database_instance.postgres_main.name}/${var.postgres_database}" # pragma: allowlist secret
}

# allow cloud run & cloud build service to access secret
resource "google_secret_manager_secret_iam_binding" "django_database_url_account_bindings" {
  project   = google_secret_manager_secret.secret_django_database_url.project
  secret_id = google_secret_manager_secret.secret_django_database_url.secret_id
  role      = "roles/secretmanager.secretAccessor"
  members = [
    "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com",
    "serviceAccount:${data.google_project.project.number}@cloudbuild.gserviceaccount.com"
  ]
}

# secret database password
resource "google_secret_manager_secret" "secret_django_database_password" {
  secret_id = "django-database-password"
  replication {
    automatic = true
  }
}

# specific version of the secret database password
resource "google_secret_manager_secret_version" "secret_django_database_password_version" {
  secret      = google_secret_manager_secret.secret_django_database_password.id
  secret_data = random_password.postgres_password.result
}

# allow cloud run & cloud build service to access secret
resource "google_secret_manager_secret_iam_binding" "django_database_password_account_bindings" {
  project   = google_secret_manager_secret.secret_django_database_password.project
  secret_id = google_secret_manager_secret.secret_django_database_password.secret_id
  role      = "roles/secretmanager.secretAccessor"
  members = [
    "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com",
    "serviceAccount:${data.google_project.project.number}@cloudbuild.gserviceaccount.com"
  ]
}

# secret gs bucket name (this might not really need to be a secret
resource "google_secret_manager_secret" "secret_django_gs_bucket_name" {
  secret_id = "django-gs-bucket-name"
  replication {
    automatic = true
  }
}

# secret gs bucket actual content
resource "google_secret_manager_secret_version" "secret_django_gs_bucket_name_version" {
  secret      = google_secret_manager_secret.secret_django_gs_bucket_name.id
  secret_data = google_storage_bucket.google_storage_bucket_static_site.name
}

# allow cloud run & cloud build service to access secret
resource "google_secret_manager_secret_iam_binding" "django_gs_bucket_name_account_bindings" {
  project   = google_secret_manager_secret.secret_django_gs_bucket_name.project
  secret_id = google_secret_manager_secret.secret_django_gs_bucket_name.secret_id
  role      = "roles/secretmanager.secretAccessor"
  members = [
    "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com",
    "serviceAccount:${data.google_project.project.number}@cloudbuild.gserviceaccount.com"
  ]
}

# create django superuser pasword
resource "random_password" "django_superuser_password" {
  length  = 24
  special = false
}

# create secret to store django superuser password
resource "google_secret_manager_secret" "secret_django_superuser_password" {
  secret_id = "django-superuser-password"
  replication {
    automatic = true
  }
}

# store django superuser password
resource "google_secret_manager_secret_version" "secret_django_superuser_password_version" {
  secret      = google_secret_manager_secret.secret_django_superuser_password.id
  secret_data = random_password.django_superuser_password.result
}

# allow cloud build service to access secret
resource "google_secret_manager_secret_iam_binding" "django_superuser_password_service_account_bindings" {
  project   = google_secret_manager_secret.secret_django_superuser_password.project
  secret_id = google_secret_manager_secret.secret_django_superuser_password.secret_id
  role      = "roles/secretmanager.secretAccessor"
  members = [
    "serviceAccount:${data.google_project.project.number}@cloudbuild.gserviceaccount.com"
  ]
}

# create secret to store sendgrid api key
resource "google_secret_manager_secret" "secret_sendgrid_api_key" {
  secret_id = "sendgrid-api-key"
  replication {
    automatic = true
  }
}

# allow cloud build service to access secret
resource "google_secret_manager_secret_iam_binding" "sendgrid_secret_api_key_service_account_bindings" {
  project   = google_secret_manager_secret.secret_sendgrid_api_key.project
  secret_id = google_secret_manager_secret.secret_sendgrid_api_key.secret_id
  role      = "roles/secretmanager.secretAccessor"
  members = [
    "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com",
    "serviceAccount:${data.google_project.project.number}@cloudbuild.gserviceaccount.com"
  ]
}



#########################################################################################################################
# artifactregistry.googleapis.com
resource "google_artifact_registry_repository" "docker_artifact_repository" {
  repository_id = "fwc"
  description   = "FWC Docker Artifact Repository"
  location      = var.gcp_region
  format        = "DOCKER"
}

# allow github service account to read
resource "google_artifact_registry_repository_iam_member" "github_service_account_docker_artifact_repostiory_read" {
  project    = google_artifact_registry_repository.docker_artifact_repository.project
  location   = google_artifact_registry_repository.docker_artifact_repository.location
  repository = google_artifact_registry_repository.docker_artifact_repository.name

  role   = "roles/artifactregistry.reader"
  member = google_service_account.github_actions_service_account.member
}

# allow github service account to write
resource "google_artifact_registry_repository_iam_member" "github_service_account_docker_artifact_repostiory_write" {
  project    = google_artifact_registry_repository.docker_artifact_repository.project
  location   = google_artifact_registry_repository.docker_artifact_repository.location
  repository = google_artifact_registry_repository.docker_artifact_repository.name

  role   = "roles/artifactregistry.writer"
  member = google_service_account.github_actions_service_account.member
}

# allow github service account to read
resource "google_artifact_registry_repository_iam_member" "serverless_robot_prod_docker_artifact_repostiory_read" {
  project    = google_artifact_registry_repository.docker_artifact_repository.project
  location   = google_artifact_registry_repository.docker_artifact_repository.location
  repository = google_artifact_registry_repository.docker_artifact_repository.name

  role   = "roles/artifactregistry.reader"
  member = "serviceAccount:service-${data.google_project.project.number}@serverless-robot-prod.iam.gserviceaccount.com"
}


#########################################################################################################################
# https://cloud.google.com/sql/docs/mysql/connect-instance-cloud-run
# this is the actual cloud run service

# this resource is overridden by the cloud deploy service which is
# triggered by github actions which is why the lifecycle ignores many
# changes

resource "google_cloud_run_v2_service" "backend_cloud_run" {
  lifecycle {
    ignore_changes = [
      template,
      labels,
    ]
  }
  name     = "cloudrun-service-backend"
  location = var.gcp_region
  ingress  = "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"

  template {
    volumes {
      name = "cloudsql"
      cloud_sql_instance {
        instances = [google_sql_database_instance.postgres_main.connection_name]
      }
    }
    containers {
      name    = "cloudrun-service-backend"
      image   = "${google_artifact_registry_repository.docker_artifact_repository.location}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.docker_artifact_repository.name}/backend:latest"
      command = ["python", "manage.py", "runserver", "0.0.0.0:8080"]

      resources {
        startup_cpu_boost = true
      }

      volume_mounts {
        name       = "cloudsql"
        mount_path = "/cloudsql"
      }
      env {
        name  = "DEBUG"
        value = "False"
      }
      env {
        name = "POSTGRES_PASSWORD"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.secret_django_database_password.secret_id
            version = google_secret_manager_secret_version.secret_django_database_password_version.version
          }
        }
      }
      env {
        name  = "POSTGRES_USER"
        value = var.postgres_user
      }
      env {
        name  = "POSTGRES_HOST"
        value = "/cloudsql/${google_sql_database_instance.postgres_main.connection_name}"
      }
      env {
        name  = "POSTGRES_PORT"
        value = ""
      }
      env {
        name  = "DJANGO_DATABASE"
        value = "production"
      }
      env {
        name = "SECRET_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.secret_django_secret_key.secret_id
            version = google_secret_manager_secret_version.secret_django_secret_key_version.version
          }
        }
      }
      env {
        name = "GS_BUCKET_NAME"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.secret_django_gs_bucket_name.secret_id
            version = google_secret_manager_secret_version.secret_django_gs_bucket_name_version.version
          }
        }
      }
      env {
        name  = "FRONTEND_HOST"
        value = "https://${var.fqdn}"
      }
      env {
        name = "SENDGRID_API_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.secret_sendgrid_api_key.secret_id
            version = "latest"
          }
        }
      }
      env {
        name  = "ALLOWED_HOST"
        value = var.fqdn
      }
    }
    timeout                          = "30s"
    max_instance_request_concurrency = 20
    scaling {
      # min_instance_count = 1
      max_instance_count = 2
    }
  }
  depends_on = [
    google_secret_manager_secret_version.secret_django_gs_bucket_name_version,
    google_secret_manager_secret_version.secret_django_database_url_version,
    google_secret_manager_secret_version.secret_django_database_password_version,
    google_secret_manager_secret_version.secret_django_secret_key_version,
  ]
}

# allow anyone (public internet) to invoke the serverless backend
#
# this is somewhat counter intuitive; but for better efficiency, the
# frontend does not proxy to the backend; instead the browser connects
# directly to the backend via the /api path on the load balancer
#
resource "google_cloud_run_service_iam_binding" "allow_anyone_to_invoke_backend" {
  location = google_cloud_run_v2_service.backend_cloud_run.location
  service  = google_cloud_run_v2_service.backend_cloud_run.name
  role     = "roles/run.invoker"
  members = [
    "allUsers"
  ]
}

# create load balancer backend service end point group
resource "google_compute_region_network_endpoint_group" "backend_neg" {
  name                  = "backend-neg"
  network_endpoint_type = "SERVERLESS"
  region                = var.gcp_region

  cloud_run {
    service = google_cloud_run_v2_service.backend_cloud_run.name
  }
}

# create load balancer backend service
resource "google_compute_backend_service" "backend_service" {
  name = "backend-service"

  protocol    = "HTTP"
  port_name   = "http"
  timeout_sec = 30

  backend {
    group = google_compute_region_network_endpoint_group.backend_neg.id
  }
  log_config {
    enable      = true
    sample_rate = 1.0
  }
}

#########################################################################################################################
# https://cloud.google.com/deploy/docs/deploy-app-run
# https://medium.com/@brodies.dev/deploying-cloud-run-workloads-with-google-cloud-deploy-e74af8e7200

# Add the clouddeploy.jobRunner role
resource "google_project_iam_binding" "cloud_deploy_jobrunner_iam_binding" {
  project = var.gcp_project_id

  members = [
    "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
  ]
  role = "roles/clouddeploy.jobRunner"
}

# Grant run.developer permissions to compute and github action
resource "google_project_iam_binding" "cloud_deploy_cloud_run_iam_binding" {
  project = var.gcp_project_id

  members = [
    "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com",
    "serviceAccount:${google_service_account.github_actions_service_account.email}"
  ]
  role = "roles/run.developer"
}


#########################################################################################################################
# https://medium.com/@brodies.dev/deploying-cloud-run-workloads-with-google-cloud-deploy-e74af8e7200
# https://cloud.google.com/deploy/docs/deploy-app-hooks

# create a delivery pipline for the backend;

# github actions push an release into this resource; in turn this
# resource deploys the service; and urns and pre/post deployment jobs
resource "google_clouddeploy_delivery_pipeline" "backend_pipeline" {
  name        = "fwc-backend"
  provider    = google-beta
  description = "FWC Backend Pipeline"
  location    = var.gcp_region
  project     = var.gcp_project_id

  serial_pipeline {
    stages {
      target_id = google_clouddeploy_target.backend_development_target.name
      strategy {
        standard {
          predeploy {
            # trigger migrate-database action before this backend goes live
            actions = ["migrate-database"]
          }
        }
      }
    }
  }
}

# this is the backend cloud deployment target
resource "google_clouddeploy_target" "backend_development_target" {
  location    = var.gcp_region
  name        = "backend-development"
  description = "Backend Development Target"

  execution_configs {
    usages            = ["RENDER", "PREDEPLOY", "DEPLOY", "POSTDEPLOY", "VERIFY"]
    execution_timeout = "3600s"
  }

  project          = var.gcp_project_id
  require_approval = false

  run {
    location = "projects/${var.gcp_project_id}/locations/${var.gcp_region}"
  }
}

#########################################################################################################################
# https://github.com/marketplace/actions/create-cloud-deploy-release
# To create and retrieve releases and rollouts
resource "google_project_iam_binding" "github_service_account_cloud_deploy_releaser_iam_binding" {
  project = var.gcp_project_id

  members = [
    "serviceAccount:${google_service_account.github_actions_service_account.email}"
  ]
  role = "roles/clouddeploy.releaser"
}

# To write release packages
resource "google_project_iam_binding" "github_service_account_storage_admin_iam_binding" {
  project = var.gcp_project_id

  members = [
    "serviceAccount:${google_service_account.github_actions_service_account.email}"
  ]
  role = "roles/storage.admin"
}

# https://registry.terraform.io/providers/hashicorp/google/latest/docs/data-sources/service_account_access_token.html

# Grant the github actions service account the ability to actAs
# *-compute@developer.gserviceaccount.com to deploy workloads into
# Cloud Run
resource "google_service_account_iam_binding" "default_execution_service_account_deploy_workloads_iam_binding" {
  service_account_id = "projects/-/serviceAccounts/${data.google_project.project.number}-compute@developer.gserviceaccount.com"

  role = "roles/iam.serviceAccountUser"

  members = [
    "serviceAccount:${google_service_account.github_actions_service_account.email}"
  ]
}
