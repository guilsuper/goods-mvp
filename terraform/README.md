# FWC Website

## Summary

Our website has two main components:

- The backend, a python [Django](https://www.djangoproject.com/) app
  (`backend/`), which runs in a serverless container in [Cloud
  Run](https://cloud.google.com/run).
- The frontend (`frontend/`), a
  [React](https://www.djangoproject.comre/) app which runs in the
  browser and is delivered from a [Cloud Storage
  Bucket](https://cloud.google.com/run).

## Build & Release

The website build is run in GitHub using [GitHub
Actions](https://github.com/features/actions)
(`.github/workflows/`). The build artifacts consist of:

- a container that is pushed into a [Docker Artifact
  Registry](https://cloud.google.com/artifact-registry)

- a release that is published in [Cloud
  Deploy](https://cloud.google.com/deploy) subsequently triggering it
  to deploy the release

These GCP interactions require authentication which is done with
[Workload Identity
Federation](https://cloud.google.com/iam/docs/workload-identity-federation).

## Deployment

Cloud Deploy is configured using
[Skaffold](https://cloud.google.com/deploy/docs/using-skaffold) found
in `/config`. These files instruct Cloud Deploy how to run the
container, including what environment variables to pass into it, how
it should scale with load, etc.

## Infrastructure as Code

The infrastructure itself is configured via
[Terraform](https://www.terraform.io/) (`terraform/`). This configures
the following:

- Public IP address
- HTTPS load balancer which maps:
  - `*` (everything) to the frontend
  - `/api` to the backend
- HTTP load balancer which redirects to HTTPS
- SSL Certificate
- Secrets to store information the backend needs to operate including:
  - Django Secret Key & Super User Password
  - Postgres Password
  - Postgres URL
  - Front End Bucket Name
  - [SendGrid](https://sendgrid.com/solutions/email-api/) API Key
- Docker Artifact Registry
- Backend (Django) Cloud Run Instance
- Frontend (React) Cloud Storage Bucket
- Cloud Deploy Resource to deploy the backend container image from the
  Docker Artifact Registry to the Cloud Run instance.
- [Cloud SQL Postgres](https://cloud.google.com/sql/docs/postgres) to
  store the tables that support Django
- GitHub Action Service Account & Associated Workload Identify Federation

In addition to the components above Terraform sets up the plumbing
between these components, and grants permissions to the necessary
service accounts.

## Tricky bits

### Pre-deploy Container

When a release is deployed to Cloud Deploy the first two things that
need to be done are to perform a database schema migration, and upload
the static files of the frontend to the Cloud Storage Bucket.

Cloud Deploy provides a `predeploy` hook for this purpose. This is a
script that runs inside a container (in this case the backend
container). On success, Cloud Deploy then spins up the backend Cloud
Run container.

Here are the two challenges:

1. The `predeploy` hook does not offer a means by which the
   environment has access to secrets.
2. The `predeploy` hook does not offer a means to connect to a
   Cloud SQL database.

### Secrets in the predeploy container

When the predeploy container starts it runs
`backend/tools/secrets_to_environment.py` (the details of how it works
can be found in the script itself). At a very high level, this script
fetches a set of secrets and stuffs those secrets into the
environment.

### Database access in the predeploy container

Google provides a tool
[cloud-sql-proxy](https://cloud.google.com/sql/docs/postgres/sql-proxy)
which uses the environments credentials to setup a secure connection
between the container it is run in and a sql backend.

`cloud-sql-proxy` is run in the background exposing the Cloud SQL
Postgres database as a unix socket for Django to connect to.

### Finally

With all of the above in place the predeploy script:

1. pushes all of the static content into the Cloud Storage Bucket.
2. migrates the necessary tables in the Cloud SQL Postgres database to
   match the table layout expected by this particular version of the
   Django backend.

## Notes

- [Overview of Cloud Deploy](https://cloud.google.com/deploy/docs/overview#the_delivery_process)
- [Cloud Deploy Terms](https://github.com/google-github-actions/create-cloud-deploy-release)
- [Website Serving in GCP Overview](https://cloud.google.com/architecture/web-serving-overview#storing_data_with_cloud_run)
- [Deploying create-react-app to S3 and CloudFront](https://wolovim.medium.com/deploying-create-react-app-to-s3-or-cloudfront-48dae4ce0af)
- [Hosting a Static Website in GCP](https://cloud.google.com/storage/docs/hosting-static-website)
- [Creating a React Production Build](https://create-react-app.dev/docs/production-build/)
- [Google Cloud Run Skaffold documentation](https://skaffold.dev/docs/deployers/cloudrun/)
- [Cloud Deploy Release Github Action](https://github.com/google-github-actions/create-cloud-deploy-release)
