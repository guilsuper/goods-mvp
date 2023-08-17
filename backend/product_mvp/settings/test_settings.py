# Copyright 2023 Free World Certified -- all rights reserved.
"""Module for custom pytest settings."""
from product_mvp.settings.settings import *  # noqa: F403, F401


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db-test.sqlite3",
    }
}
