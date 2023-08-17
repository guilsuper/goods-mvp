# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains healthcheck test."""
import pytest
from django.test import Client


@pytest.mark.django_db()
def test_smoke(client: Client):
    """The healthcheck test."""
    response = client.get("/api/")
    assert response.status_code == 200
