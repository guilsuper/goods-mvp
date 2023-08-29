# Copyright 2023 Free World Certified -- all rights reserved.
"""Module with serializers."""
from api.models import Company
from rest_framework.serializers import ModelSerializer


class CompanySerializer(ModelSerializer):
    """Company base serializer."""

    class Meta:
        """Meta class for company serializer."""

        model = Company
        fields = (
            "name",
            "website",
            "jurisdiction",
        )

    def create(self, validated_data):
        """Overwritten create method for setting up the slug."""

        company = Company.objects.create(
            **validated_data,
        )
        # Set company slug
        company.set_slug()
        company.save()

        return company

    def update(self, instance, validated_data):
        """Overwritten update method for setting up the slug field."""
        instance = super().update(instance, validated_data)

        if "name" in validated_data.keys():
            instance.set_slug()
            instance.save()

        return instance


class CompanyRetrieveSerializer(ModelSerializer):
    """Company retrieve serializer."""

    class Meta:
        """Meta class for company serializer."""

        model = Company
        fields = (
            "name",
            "website",
            "jurisdiction",
            "slug"
        )
