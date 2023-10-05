# Copyright 2023 Free World Certified -- all rights reserved.
"""Module with serializers."""
from api.models import Administrator
from api.serializers import CompanyRetrieveSerializer
from django.contrib.auth.models import Group
from rest_framework.serializers import BooleanField
from rest_framework.serializers import CharField
from rest_framework.serializers import ModelSerializer


class GroupSerializer(ModelSerializer):
    """User groups serializer."""

    class Meta:
        """Metaclass for serializer, to retrieve only group name."""

        model = Group
        fields = ("name",)


class AdministratorSerializer(ModelSerializer):
    """Administrator base serilizer."""

    is_active = BooleanField(read_only=True)
    groups = GroupSerializer(many=True, read_only=True)
    company = CompanyRetrieveSerializer(read_only=True)

    password = CharField(max_length=128, write_only=True)

    class Meta:
        """Metaclass for the AdministratorSerializer."""

        model = Administrator

        # Serializer sets company field in create method
        fields = (
            "password", "email",
            "first_name", "last_name",
            "groups", "company", "is_active",
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


class PMSerializer(ModelSerializer):
    """PM base serilizer."""

    is_active = BooleanField(read_only=True)
    groups = GroupSerializer(many=True, read_only=True)
    company = CompanyRetrieveSerializer(read_only=True)

    password = CharField(max_length=128, write_only=True)

    class Meta:
        """Metaclass for the PMSerializer."""

        model = Administrator
        fields = (
            "password", "email",
            "first_name", "last_name",
            "groups", "company", "is_active",
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
