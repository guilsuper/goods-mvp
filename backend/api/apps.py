# Copyright 2023 Free World Certified -- all rights reserved.
"""Module with API configurations."""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """API configurations."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
