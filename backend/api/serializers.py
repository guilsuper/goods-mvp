"""Module with serializers."""

from api.models import Administrator, Product

from rest_framework.serializers import ModelSerializer


class ProductSerializer(ModelSerializer):
    """Product basic serilizer."""

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
        return Administrator.objects.create_user(**validated_data)

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
        )
