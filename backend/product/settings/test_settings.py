# Copyright 2023 Free World Certified -- all rights reserved.
"""Module for custom pytest settings."""
import os

from product.settings.settings import *  # noqa: F403, F401


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db-test.sqlite3",
    },
}

GS_QUERYSTRING_AUTH = False

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
