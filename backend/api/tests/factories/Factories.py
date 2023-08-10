# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains Product and Administrator factories."""
from datetime import date

import factory
from django.contrib.auth.models import Group
from factory.django import DjangoModelFactory


class GroupFactory(factory.django.DjangoModelFactory):
    """Factory for group default model."""

    class Meta:
        """Defined model and fields for Group factory."""
        model = Group
        django_get_or_create = ("name", )

    name = "Administrator"

    # Add a "name" attribute to the factory that allows passing a custom name
    @classmethod
    def get_or_create(cls, **kwargs):
        """Gets or creates a groups."""
        name = kwargs.pop("name", None)
        group = super().create(**kwargs)
        if name:
            group.name = name
            group.save()
        return group


class AdministratorFactory(DjangoModelFactory):
    """Administrator factory (groups is Administrator)."""

    class Meta:
        """Defined model to use Administrator factory."""
        model = "api.Administrator"

    username = factory.Sequence(lambda n: f"Admin {n}")
    password = factory.PostGenerationMethodCall("set_password", "admin")
    company_name = factory.Sequence(lambda n: f"Company {n}")
    company_address = factory.Sequence(lambda n: str(n) * 8)
    company_size = 123
    industry = factory.Sequence(lambda n: str(n) * 8)
    first_name = factory.Sequence(lambda n: str(n) * 8)
    last_name = factory.Sequence(lambda n: str(n) * 8)
    email = factory.Sequence(lambda n: str(n) * 8 + "@gmail.com")
    phonenumber = "+380999999999"
    is_active = True
    boss = None

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        """Group setup for Administrator object."""
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)


class ProductFactory(DjangoModelFactory):
    """Product factory."""

    class Meta:
        """Product factory model and fields."""

        model = "api.Product"
        django_get_or_create = (
            "sku_id", "public_facing_id", "public_facing_name",
            "description", "sctr_date", "sctr_cogs",
            "cogs_coutry_recipients", "product_input_manufacturer",
            "product_input_type", "owner"
        )

    sku_id = factory.Sequence(lambda n: int(str(n) * 8))
    public_facing_id = factory.Sequence(lambda n: int(str(n) * 8))
    public_facing_name = factory.Sequence(lambda n: int(str(n) * 8))
    description = "why"

    sctr_date = date(2019, 1, 1)
    sctr_cogs = 50.0
    cogs_coutry_recipients = "BH"

    product_input_manufacturer = "AAAA"
    product_input_type = "Art"

    owner = factory.SubFactory(AdministratorFactory)
