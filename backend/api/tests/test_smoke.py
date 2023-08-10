"""Module contains healthcheck test."""
from django.test import Client
from django.test import TestCase


class TestSmoke(TestCase):
    """Healthcheck test."""

    def setUp(self):
        """Client setup."""
        self.client = Client()

    def test_smoke(self):
        """The healthcheck test."""
        response = self.client.get("/api/")
        self.assertEqual(response.status_code, 200)
