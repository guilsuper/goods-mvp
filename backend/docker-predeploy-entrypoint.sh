#!/bin/bash -e

# Copyright 2023 Free World Certified -- all rights reserved.

/backend/tools/secrets_to_environment.py >/tmp/gcp_secrets.sh
source /tmp/gcp_secrets.sh
rm /tmp/gcp_secrets.sh

INSTANCE_CONNECTION_NAME=$CLOUD_RUN_PROJECT:$CLOUD_RUN_LOCATION:postgres-main-instance

/usr/bin/cloud-sql-proxy $INSTANCE_CONNECTION_NAME --unix-socket /cloudsql &

# Push static content to GCP Bucket
python manage.py collectstatic --no-input

# Migrate the database
python manage.py migrate
