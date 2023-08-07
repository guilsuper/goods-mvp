"""Module with serializers."""

from api.models import Administrator, Product

from django.contrib.auth.models import Group

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class ProductCreateSerializer(ModelSerializer):
    """Product basic serilizer."""

    class Meta:
        """Metaclass for the ProductSerializer."""

        model = Product
        exclude = ("id", "owner")

    def create(self, validated_data):
        """Overwritten create method for setting up the product owner."""
        user = self.context["request"].user
        validated_data["owner"] = user.boss if user.groups.filter(
            name="PM"
        ).exists() else user

        return super().create(validated_data)


class ProductGetSerializer(ModelSerializer):
    """Product basic serilizer."""

    owner = serializers.CharField(source="owner.username")

    class Meta:
        """Metaclass for the ProductSerializer."""

        model = Product
        exclude = ("id", )


class AdministratorSerializer(ModelSerializer):
    """Administrator base serilizer."""

    class Meta:
        """Metaclass for the AdministratorSerializer."""

        model = Administrator
        fields = (
            "username", "password", "company_name",
            "company_address", "industry", "company_size",
            "first_name", "last_name", "email",
            "phonenumber",
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

    class Meta:
        """Metaclass for the AdministratorRetrieveSerializer."""

        model = Administrator
        fields = (
            "username", "company_name", "company_address",
            "industry", "company_size", "first_name",
            "last_name", "email", "phonenumber",
            "boss"
        )


class PMRetrieveSerializer(ModelSerializer):
    """PM retrieve serilizer."""
    boss = serializers.CharField(source="boss.username")

    class Meta:
        """Metaclass for the PMRetrieveSerializer."""

        model = Administrator
        fields = (
            "username", "company_name", "company_address",
            "industry", "company_size", "first_name",
            "last_name", "email", "phonenumber",
            "boss", "is_active"
        )


class PMSerializer(ModelSerializer):
    """PM base serilizer."""

    class Meta:
        """Metaclass for the PMSerializer."""

        model = Administrator
        fields = (
            "username", "phonenumber", "password",
            "first_name", "last_name", "email",
        )

    def create(self, validated_data):
        """Overwritten create method for PMSerializer."""
        validated_data["is_active"] = False

        boss = self.context["request"].user
        validated_data["boss"] = boss

        validated_data["company_name"] = boss.company_name
        validated_data["company_address"] = boss.company_address
        validated_data["industry"] = boss.industry
        validated_data["company_size"] = boss.company_size

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
