# Copyright 2023 Free World Certified -- all rights reserved.
"""Module with serializers."""
from api.models import Country
from free_world_countries import freedom_house_country_name_url_framents
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField


class CountrySerializer(ModelSerializer):
    """Country base serializer."""

    freedom_house_url_name = SerializerMethodField(read_only=True)

    class Meta:
        """Meta class for country serializer."""

        model = Country
        fields = "__all__"

    def get_freedom_house_url_name(self, obj) -> str:
        return freedom_house_country_name_url_framents[obj.alpha_2].fragment
