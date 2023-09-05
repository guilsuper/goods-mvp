# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains SCTR and Administrator factories."""
import factory
from api.models import SCTR_ID_TYPES
from api.models import SCTR_STATES
from api.models import SOURCE_COMPONENT_TYPE
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


class CompanyFactory(DjangoModelFactory):
    """Company factory."""

    class Meta:
        """Defined model to use Company factory."""
        model = "api.Company"

    website = factory.Sequence(lambda n: f"Company{n}.com")
    name = factory.Sequence(lambda n: f"St. Company, {n}")

    jurisdiction = factory.Sequence(lambda n: f"St. Admin, {n}")


class AdministratorFactory(DjangoModelFactory):
    """Administrator factory (groups is Administrator)."""

    class Meta:
        """Defined model to use Administrator factory."""
        model = "api.Administrator"

        # DjangoModelFactory in future will stop issuing
        # a second call to save() on the created instance when
        # Post-generation hooks return a value (method 'group')
        # Appropriate warning is displayed if this setting is missing
        # according to the official changeLog 3.3.0 (2023-07-19)
        # https://factoryboy.readthedocs.io/en/stable/changelog.html
        skip_postgeneration_save = True

    password = factory.PostGenerationMethodCall("set_password", "admin")

    first_name = factory.Sequence(lambda n: str(n) * 8)
    last_name = factory.Sequence(lambda n: str(n) * 8)
    email = factory.Sequence(lambda n: str(n) * 8 + "@gmail.com")
    is_active = True

    company = factory.SubFactory(CompanyFactory)

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        """Group setup for Administrator object."""
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)


class SCTRFactory(DjangoModelFactory):
    """SCTR factory."""

    class Meta:
        """SCTR factory model and fields."""

        model = "api.SCTR"

    unique_identifier = factory.Sequence(lambda n: int(str(n) * 8))
    unique_identifier_type = SCTR_ID_TYPES.SKU
    marketing_name = factory.Sequence(lambda n: int(str(n) * 8))
    version = 1
    state = SCTR_STATES.PUBLISHED
    cogs = 100

    company = factory.SubFactory(CompanyFactory)


class ComponentFactory(DjangoModelFactory):
    """SourceComponent factory."""

    class Meta:
        """Component factory model and fields."""

        model = "api.SourceComponent"

    fraction_cogs = 100
    marketing_name = factory.Sequence(lambda n: int(str(n) * 8))
    component_type = SOURCE_COMPONENT_TYPE.EXTERNALLY_SOURCED
    country_of_origin = "USA"
    external_sku = factory.Sequence(lambda n: int(str(n) * 8))
    parent_sctr = factory.SubFactory(SCTRFactory)
