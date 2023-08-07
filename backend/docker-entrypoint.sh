#!/bin/bash -e

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Start the Django application (adjust this command based on your project's setup)
exec "$@"
