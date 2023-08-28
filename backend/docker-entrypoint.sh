#!/bin/bash -e

# Copyright 2023 Free World Certified -- all rights reserved.

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Start the Django application (adjust this command based on your project's setup)
exec "$@"
