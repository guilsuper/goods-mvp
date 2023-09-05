output "lb-address" {
  description = "The load balancer IP address (used in Cloud DNS)"
  value       = google_compute_global_address.external_ip_address.address
}

output "project_number" {
  description = "This is the current project number"
  value       = data.google_project.project.number
}

output "github_workload_identity_provider_name" {
  description = "The Github Workload Identity Provier Name (used in github action)"
  value       = google_iam_workload_identity_pool_provider.github_workload_identity_pool_provider.name
}

output "github_actions_service_account_email" {
  description = "The GitHub Actions Service Account Email  (used in github action)"
  value       = google_service_account.github_actions_service_account.email
}

output "django_superuser_password" {
  description = "The Django superuser password"
  value       = random_password.django_superuser_password.result

  # the output is intentionally obfuscated it can be viewed with
  # terraform output -json
  sensitive = true
}
