# Copyright 2023 Free World Certified -- all rights reserved.
"""Module with serializers."""
from api.models import Administrator
from api.models import Company
from api.models import Product
from django.contrib.auth.models import Group
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


class GroupSerializer(ModelSerializer):
    """User groups serializer."""

    class Meta:
        """Metaclass for serializer, to retrieve only group name."""

        model = Group
        fields = ("name",)


class ProductCreateSerializer(ModelSerializer):
    """Product basic serilizer."""

    class Meta:
        """Metaclass for the ProductSerializer."""

        model = Product
        exclude = ("id", "company")

    def create(self, validated_data):
        """Overwritten create method for setting up the product company."""
        user = self.context["request"].user

        validated_data["company"] = user.company

        return super().create(validated_data)


class ProductGetSerializer(ModelSerializer):
    """Product basic serilizer."""

    company = CompanySerializer()

    class Meta:
        """Metaclass for the ProductSerializer."""

        model = Product
        exclude = ("id", )


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
