# Copyright 2023 Free World Certified -- all rights reserved.
"""Contains pytest configurations."""
import pytest
from product_mvp import settings


pytest_plugins = ["api.tests.fixtures"]


@pytest.fixture(scope="session")
def django_db_setup():
    """Override django DB setup for tests."""
    # Database for testing purpose
    # So the production or development databases aren't involved
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
        "ATOMIC_REQUESTS": True
    }
