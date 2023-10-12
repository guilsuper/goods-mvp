# Copyright 2023 Free World Certified -- all rights reserved.
"""Module for development settings."""
import os

from product.settings.settings import *  # noqa: F403, F401

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
}

MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # noqa: F405

STATICFILES_DIRS = []
