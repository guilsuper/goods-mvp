# Copyright 2023 Free World Certified -- all rights reserved.
"""Module with serializers."""
from api.models import Administrator
from api.models import Company
from api.models import SCTR
from api.models import SCTR_ID_TYPES
from api.models import SCTR_STATES
from api.models import SOURCE_COMPONENT_TYPE
from api.models import SourceComponent
from django.contrib.auth.models import Group
from django_countries.serializers import CountryFieldMixin
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError


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


class GroupSerializer(ModelSerializer):
    """User groups serializer."""

    class Meta:
        """Metaclass for serializer, to retrieve only group name."""

        model = Group
        fields = ("name",)


class SourceComponentSerializer(CountryFieldMixin, ModelSerializer):
    """Source Component base serializer."""

    class Meta:
        """Metaclass for the SourceComponentSerializer."""

        model = SourceComponent
        exclude = ("id", "parent_sctr")

    def validate(self, attrs):
        """Validate component type and data."""
        if attrs["component_type"] == SOURCE_COMPONENT_TYPE.externally_sourced:
            # Should be only external_sku
            if "external_sku" not in attrs.keys() or "country_of_origin" in attrs.keys():
                raise ValidationError("External sku is required for externally sourced type.")
        elif attrs["component_type"] == SOURCE_COMPONENT_TYPE.made_in_house:
            # Should be only country_of_origin
            if "external_sku" in attrs.keys() or "country_of_origin" not in attrs.keys():
                raise ValidationError("Country of origin is required for made in house type.")
        return super().validate(attrs)


class SCTRSerializer(ModelSerializer):
    """SCTR basic serilizer."""

    components = SourceComponentSerializer(many=True)

    class Meta:
        """Metaclass for the SCTRSerializer."""

        model = SCTR
        fields = (
            "unique_identifier_type",
            "unique_identifier",
            "marketing_name",
            "components"
        )

    def validate(self, attrs):
        """Validation for GNIT type, COGS."""

        # For an UpdateView check if field exists
        # CreateView automatically check if field exists
        if "unique_identifier_type" in attrs.keys():
            if attrs["unique_identifier_type"] == SCTR_ID_TYPES.GNIT:
                if attrs["unique_identifier"].isnumeric():
                    raise ValidationError("GNIT must contain only integers.")
                if len(attrs["unique_identifier"]) != 13:
                    raise ValidationError("GNIT must contain 13 digits.")

        # For an UpdateView if field exists
        # CreateView automatically check if field exists
        if "components" in attrs:
            if sum([component["fraction_cogs"] for component in attrs["components"]]) != 100:
                raise ValidationError("Sum of COGS must be 100.")

        return super().validate(attrs)

    def create(self, validated_data):
        """Overwritten create method for setting up the product info."""
        # Setup state
        validated_data["state"] = SCTR_STATES.published
        # Setup cogs (they were checked in validation method)
        validated_data["sctr_cogs"] = 100
        # Setup company
        user = self.context["request"].user
        validated_data["company"] = user.company

        components = validated_data.pop("components")

        sctr = SCTR.objects.create(**validated_data)
        # Create each component
        for component in components:
            SourceComponent.objects.create(parent_sctr=sctr, **component)

        return sctr

    def update(self, instance, validated_data):
        """Method to update nested components."""

        # Remove current components
        SourceComponent.objects.filter(parent_sctr=instance).delete()
        components = validated_data.pop("components")

        # Create each component
        for component in components:
            SourceComponent.objects.create(parent_sctr=instance, **component)

        return super().update(instance, validated_data)


class SCTRGetSerializer(ModelSerializer):
    """SCTR get serilizer."""

    company = CompanySerializer()
    components = SourceComponentSerializer(many=True, read_only=True)

    class Meta:
        """Metaclass for the SCTRSerializer."""

        model = SCTR
        fields = (
            "unique_identifier",
            "marketing_name",
            "unique_identifier_type",
            "version",
            "state",
            "sctr_cogs",
            "company",
            "components"
        )


class AdministratorSerializer(ModelSerializer):
    """Administrator base serilizer."""

    class Meta:
        """Metaclass for the AdministratorSerializer."""

        model = Administrator

        # Serializer sets company field in create method
        fields = (
            "password", "email",
            "first_name", "last_name"
        )

    def create(self, validated_data):
        """Overwritten create method for AdministratorSerializer."""
        validated_data["is_active"] = False

        admin = Administrator.objects.create_user(
            **validated_data,
        )
        # Add admin to group
        group, _ = Group.objects.get_or_create(name="Administrator")
        group.user_set.add(admin)

        return admin

    def update(self, instance, validated_data):
        """Overwritten update method for AdministratorSerializer."""
        instance = super().update(instance, validated_data)

        if "password" in validated_data.keys():
            instance.update_password(validated_data["password"])

        return instance


class AdministratorRetrieveSerializer(ModelSerializer):
    """Administrator retrieve serilizer."""

    groups = GroupSerializer(many=True)
    company = CompanyRetrieveSerializer()

    class Meta:
        """Metaclass for the AdministratorRetrieveSerializer."""

        model = Administrator
        exclude = (
            "id", "is_superuser", "is_staff", "user_permissions"
        )


class PMRetrieveSerializer(ModelSerializer):
    """PM retrieve serilizer."""

    groups = GroupSerializer(many=True)
    company = CompanySerializer()

    class Meta:
        """Metaclass for the PMRetrieveSerializer."""

        model = Administrator
        exclude = (
            "id", "is_superuser", "is_staff", "user_permissions"
        )


class PMSerializer(ModelSerializer):
    """PM base serilizer."""

    class Meta:
        """Metaclass for the PMSerializer."""

        model = Administrator
        fields = (
            "password", "email",
            "first_name", "last_name"
        )

    def create(self, validated_data):
        """Overwritten create method for PMSerializer."""
        validated_data["is_active"] = False

        validated_data["company"] = self.context["request"].user.company

        # Add pm to group
        pm = Administrator.objects.create_user(**validated_data)
        group, _ = Group.objects.get_or_create(name="PM")
        group.user_set.add(pm)

        return pm

    def update(self, instance, validated_data):
        """Overwritten update method for PMSerializer."""
        instance = super().update(instance, validated_data)

        if "password" in validated_data.keys():
            instance.update_password(validated_data["password"])

        return instance
