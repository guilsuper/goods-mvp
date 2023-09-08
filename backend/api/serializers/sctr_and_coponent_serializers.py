# Copyright 2023 Free World Certified -- all rights reserved.
"""Module with serializers."""
from api.models import SCTR
from api.models import SCTR_ID_TYPES
from api.models import SCTR_STATES
from api.models import SOURCE_COMPONENT_TYPE
from api.models import SourceComponent
from api.serializers import CompanySerializer
from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin
from rest_framework.serializers import BooleanField
from rest_framework.serializers import CharField
from rest_framework.serializers import ChoiceField
from rest_framework.serializers import FloatField
from rest_framework.serializers import IntegerField
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ValidationError


class ComponentTypeToString(ChoiceField):
    """ChoiceField that converts integer to string representation."""

    def to_representation(self, obj):
        # Convert integer to string
        return SOURCE_COMPONENT_TYPE(obj).name


class UniqueIdentifierTypeToString(ChoiceField):
    """ChoiceField that converts integer to string representation."""

    def to_representation(self, obj):
        # Convert integer to string
        return SCTR_ID_TYPES(obj).name


class SCTRStateToString(ChoiceField):
    """ChoiceField that converts integer to string representation."""

    def to_representation(self, obj):
        # Convert integer to string
        return SCTR_STATES(obj).name


class SourceComponentSerializer(CountryFieldMixin, ModelSerializer):
    """Source Component create and get serializer."""

    id = IntegerField(read_only=True)
    # To make it required
    marketing_name = CharField(required=True, max_length=500)
    # To make component type readable for frontend developers
    component_type_str = CharField(max_length=18, write_only=True)
    # Transforms component_type to string in the response
    component_type = ComponentTypeToString(choices=SOURCE_COMPONENT_TYPE.choices(), read_only=True)
    # To make it required
    fraction_cogs = FloatField(required=True)
    # To make it required
    country_of_origin = CountryField(required=True, name_only=True)
    # To allow blank if MADE_IN_HOUSE
    # Additional validation in validate method
    external_sku = CharField(max_length=25, allow_blank=True)

    class Meta:
        """Metaclass for the SourceComponentSerializer."""

        model = SourceComponent
        exclude = ("parent_sctr", )

    def validate_fraction_cogs(self, value):
        """Check if greater than 0."""
        if value <= 0:
            raise ValidationError("Should be more then 0")
        return value

    def validate_component_type_str(self, value):
        """Custom validation to convert string component type to integer."""
        try:
            # Map the string value to the corresponding integer value from SCTR_ID_TYPES
            return SOURCE_COMPONENT_TYPE[value.upper()]
        except KeyError:
            raise ValidationError("Invalid component_type")

    def validate(self, attrs):
        """Validate component type and data."""
        if "component_type_str" not in attrs:
            raise ValidationError("component_type_str is required.")

        if attrs["component_type_str"] == "EXTERNALLY_SOURCED":
            # Should be only external_sku and country of origin should be None
            if "external_sku" not in attrs.keys():
                raise ValidationError("External sku is required for externally sourced type.")
            # Remove whitespaces and check if other characters left
            if len(attrs["external_sku"].strip()) == 0:
                raise ValidationError("External sku may not be blank.")
        return super().validate(attrs)

    def create(self, validated_data):
        """Adds component type."""
        validated_data["component_type"] = validated_data.pop("component_type_str")
        return super().create(validated_data)


class SourceComponentDraftSerializer(CountryFieldMixin, ModelSerializer):
    """Source Component 'create a draft' and upddate serializer."""

    id = IntegerField(read_only=True)
    # Transforms component_type to readable string
    component_type_str = CharField(
        max_length=18,
        write_only=True,
        required=False,
        allow_blank=True
    )
    component_type = ComponentTypeToString(
        choices=SOURCE_COMPONENT_TYPE.choices(),
        read_only=True
    )
    # To display a country full name instead of a code
    country_of_origin = CountryField(required=False, name_only=True, allow_blank=True)
    # To allow this field be blank
    external_sku = CharField(max_length=25, required=False, allow_blank=True)

    class Meta:
        """Metaclass for the SourceComponent draft Serializer."""

        model = SourceComponent
        exclude = ("parent_sctr", )

    def validate_fraction_cogs(self, value):
        """Check if greater than 0."""
        if value < 0:
            raise ValidationError("Should be more or equal to 0")
        return value

    def validate_component_type_str(self, value):
        """Custom validation to convert string component type to integer."""
        try:
            # Map the string value to the corresponding integer value from SCTR_ID_TYPES
            return SOURCE_COMPONENT_TYPE[value.upper()]
        except KeyError:
            # Set default
            return SOURCE_COMPONENT_TYPE["MADE_IN_HOUSE"]

    def create(self, validated_data):
        """Adds component type."""
        validated_data["component_type"] = validated_data.pop("component_type_str")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Adds component type."""
        validated_data["component_type"] = validated_data.pop("component_type_str")
        return super().update(instance, validated_data)


class SCTRCreateGetSerializer(ModelSerializer):
    """SCTR 'create and publish' and get serilizer."""

    # To define a list of components in POST request
    components = SourceComponentSerializer(many=True)
    # To make this field required
    marketing_name = CharField(max_length=500)
    # To make unique_identifier_type as string
    unique_identifier_type_str = CharField(max_length=4, write_only=True)

    # Read only fields
    company = CompanySerializer(read_only=True)
    id = IntegerField(read_only=True)
    version = IntegerField(read_only=True)
    state = SCTRStateToString(choices=SCTR_STATES.choices(), read_only=True)
    cogs = FloatField(read_only=True)
    unique_identifier_type = UniqueIdentifierTypeToString(
        choices=SCTR_ID_TYPES,
        read_only=True
    )
    is_latest_version = BooleanField(read_only=True)

    class Meta:
        """Metaclass for the SCTRCreateSerializer."""

        model = SCTR
        fields = (

            "unique_identifier_type_str",
            "unique_identifier",
            "marketing_name",
            "components",

            # Read only
            "id",
            "company",
            "version",
            "state",
            "cogs",
            "unique_identifier_type",
            "is_latest_version"
        )

    def validate_unique_identifier_type_str(self, value):
        """Custom validation to convert string identifier type to integer."""
        try:
            # Map the string value to the corresponding integer value from SCTR_ID_TYPES
            return SCTR_ID_TYPES[value.upper()]
        except KeyError:
            raise ValidationError("Invalid unique_identifier_type")

    def validate(self, attrs):
        """Validation for GNIT type, COGS."""

        if attrs["unique_identifier_type_str"] == "GNIT":
            if not attrs["unique_identifier"].isnumeric():
                raise ValidationError("GNIT must contain only integers.")
            if len(attrs["unique_identifier"]) != 13:
                raise ValidationError("GNIT must contain 13 digits.")

        cogs = sum([
            component["fraction_cogs"]
            for component in attrs["components"]
            if "fraction_cogs" in component and component["fraction_cogs"]
        ])
        if cogs != 100:
            raise ValidationError("Sum of COGS must be 100.")

        return super().validate(attrs)

    def create(self, validated_data):
        """Overwritten create method for setting up the SCTR info."""
        # Setup state
        validated_data["state"] = SCTR_STATES.PUBLISHED
        # Setup COGS (they were checked in validation method)
        validated_data["cogs"] = 100
        # Setup unique identifier field from string
        validated_data["unique_identifier_type"] = validated_data.pop("unique_identifier_type_str")
        # Setup company
        user = self.context["request"].user
        validated_data["company"] = user.company
        # Set as latest version
        validated_data["is_latest_version"] = True
        # Create components separately
        components = validated_data.pop("components")

        sctr = SCTR.objects.create(**validated_data)
        # Create each component
        for component in components:
            component["component_type"] = component.pop("component_type_str")
            SourceComponent.objects.create(parent_sctr=sctr, **component)

        return sctr


class SCTRDraftSerializer(ModelSerializer):
    """SCTR creating draft serilizer."""

    components = SourceComponentDraftSerializer(many=True)
    marketing_name = CharField(max_length=500, allow_blank=True, required=False)

    class Meta:
        """Metaclass for the SCTRDraftSerializer."""

        model = SCTR
        fields = (
            "unique_identifier_type",
            "unique_identifier",
            "marketing_name",
            "components"
        )

    def create(self, validated_data):
        """Overwritten create method for setting up the SCTR info."""
        # Setup state
        validated_data["state"] = SCTR_STATES.DRAFT
        # Setup cogs, if no components -- set to 0
        validated_data["cogs"] = 0
        # Setup company
        user = self.context["request"].user
        validated_data["company"] = user.company
        # Set as latest version
        validated_data["is_latest_version"] = True

        if "components" in validated_data:
            components_data = validated_data.pop("components")

        sctr = SCTR.objects.create(**validated_data)
        # If there are components - update cogs and create components
        if components_data:
            sctr.cogs = sum([
                component["fraction_cogs"]
                for component in components_data
                if "fraction_cogs" in component and component["fraction_cogs"]
            ])
            # To save COGS update
            sctr.save()
            # Create each component
            for component in components_data:
                if "component_type_str" in component:
                    component["component_type"] = component.pop("component_type_str")
                SourceComponent.objects.create(parent_sctr=sctr, **component)

        return sctr


class SCTRPublishValidatorSerializer(ModelSerializer):
    """Validates the SCTR before moving it to the published state."""

    class Meta:
        """Meta class for SCTR serializer."""

        model = SCTR
        fields = (
            "unique_identifier",
            "marketing_name",
            "unique_identifier_type",
        )

    def validate(self, attrs):
        """Validation for GNIT type."""

        if attrs["unique_identifier_type"] == "GNIT":
            if not attrs["unique_identifier"].isnumeric():
                raise ValidationError("GNIT must contain only integers.")
            if len(attrs["unique_identifier"]) != 13:
                raise ValidationError("GNIT must contain 13 digits.")

        return super().validate(attrs)
