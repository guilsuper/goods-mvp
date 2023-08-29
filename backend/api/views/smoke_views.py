# Copyright 2023 Free World Certified -- all rights reserved.
"""API smoke view module."""
from rest_framework.generics import ListAPIView
from rest_framework.response import Response


class Smoke(ListAPIView):
    """Backend healthcheck."""

    def get(self, request):
        """Retrieving basic response."""
        return Response("Working as intended.")
