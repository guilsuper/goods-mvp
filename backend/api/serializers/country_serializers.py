# Copyright 2023 Free World Certified -- all rights reserved.
"""Module with serializers."""
from api.models import Country
from rest_framework.serializers import ModelSerializer


class CountrySerializer(ModelSerializer):
    """Country base serializer."""

    class Meta:
        """Meta class for country serializer."""

        model = Country
        fields = "__all__"
