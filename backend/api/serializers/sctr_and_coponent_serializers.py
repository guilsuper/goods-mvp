# Copyright 2023 Free World Certified -- all rights reserved.
"""Module with serializers."""
from api.models import SCTR
from api.models import SCTR_ID_TYPES
from api.models import SCTR_STATES
from api.models import SOURCE_COMPONENT_TYPE
from api.models import SourceComponent
from api.serializers import CompanySerializer
from django_countries.serializers import CountryFieldMixin
from rest_framework.serializers import CharField
from rest_framework.serializers import FloatField
from rest_framework.serializers import IntegerField
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError


class SourceComponentSerializer(CountryFieldMixin, ModelSerializer):
    """Source Component base serializer."""

    id = IntegerField(read_only=True)
    marketing_name = CharField(max_length=500)
    fraction_cogs = FloatField()

    class Meta:
        """Metaclass for the SourceComponentSerializer."""

        model = SourceComponent
        exclude = ("parent_sctr", )

    def validate(self, attrs):
        """Validate component type and data."""
        if attrs["component_type"] == SOURCE_COMPONENT_TYPE.externally_sourced:
            # Should be only external_sku and country of origin should be None
            if "external_sku" not in attrs.keys() and attrs["country_of_origin"]:
                raise ValidationError("External sku is required for externally sourced type.")
            # Set country_of_origin to None
            attrs["country_of_origin"] = None

        elif attrs["component_type"] == SOURCE_COMPONENT_TYPE.made_in_house:
            # Should be only country_of_origin
            if "country_of_origin" not in attrs.keys() and attrs["external_sku"]:
                raise ValidationError("Country of origin is required for made in house type.")
            attrs["external_sku"] = None
        return super().validate(attrs)


class SourceComponentDraftSerializer(CountryFieldMixin, ModelSerializer):
    """Source Component draft serializer."""

    id = IntegerField(read_only=True)

    class Meta:
        """Metaclass for the SourceComponent draft Serializer."""

        model = SourceComponent
        exclude = ("parent_sctr", )


class SCTRCreateSerializer(ModelSerializer):
    """SCTR basic serilizer."""

    components = SourceComponentSerializer(many=True)
    marketing_name = CharField(max_length=500)

    class Meta:
        """Metaclass for the SCTRCreateSerializer."""

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
                if not attrs["unique_identifier"].isnumeric():
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


class SCTRSerializer(ModelSerializer):
    """SCTR basic serilizer."""

    class Meta:
        """Metaclass for the SCTRSerializer."""

        model = SCTR
        fields = (
            "unique_identifier",
            "marketing_name",
            "unique_identifier_type",
        )


class SCTRGetSerializer(ModelSerializer):
    """SCTR get serilizer."""

    company = CompanySerializer()
    components = SourceComponentSerializer(many=True, read_only=True)

    class Meta:
        """Metaclass for the SCTRGetSerializer."""

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


class SCTRDraftCreateSerializer(ModelSerializer):
    """SCTR creating draft serilizer."""

    components = SourceComponentDraftSerializer(many=True, required=False)
    unique_identifier = CharField(max_length=25, required=True)

    class Meta:
        """Metaclass for the SCTRDraftCreateSerializer."""

        model = SCTR
        fields = (
            "unique_identifier_type",
            "unique_identifier",
            "marketing_name",
            "components"
        )

    def create(self, validated_data):
        """Overwritten create method for setting up the product info."""
        # Setup state
        validated_data["state"] = SCTR_STATES.draft
        # Setup cogs, if no components -- set to 0
        validated_data["sctr_cogs"] = 0
        # Setup company
        user = self.context["request"].user
        validated_data["company"] = user.company

        # If there are components - update cogs and create components
        if "components" in validated_data:
            components = validated_data.pop("components")

            validated_data["sctr_cogs"] = sum([
                component["fraction_cogs"]
                for component in components
                if "fraction_cogs" in component
            ])

            sctr = SCTR.objects.create(**validated_data)
            # Create each component
            for component in components:
                SourceComponent.objects.create(parent_sctr=sctr, **component)

        return sctr


class SCTRPublishValidatorSerializer(ModelSerializer):
    """Validates the product before moving it to the published state."""

    class Meta:
        """Meta class for SCTR serializer."""

        model = SCTR
        fields = (
            "marketing_name",
            "unique_identifier_type",
        )
