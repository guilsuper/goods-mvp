# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains database tables as models."""
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.core.validators import RegexValidator
from django.db import models
from django.template.defaultfilters import slugify
from django_countries.fields import CountryField


full_domain_validator = RegexValidator(
    r"[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9](?:\.[a-zA-Z]{2,})+",
    "Invalid domain, it should be like example.com.eu or example.com"
)


class PRODUCT_TYPES(models.TextChoices):
    """Allowed coices for product types."""

    convenience_goods = "Convenience Goods"
    raw_materials = "Raw Materials"
    component_parts = "Component Parts"
    software = "Software"
    hardware = "Hardware"
    consumer_electronics = "Consumer Electronics"
    cookware = "Cookware"
    appliances = "Appliances"
    homegoods = "Homegoods"
    clothing = "Clothing"
    jewelry = "Jewelry"
    art = "Art"


class SCTR_ID_TYPES(models.TextChoices):
    """Allowed coices for SCTR unique id types."""

    SKU = "SKU"
    GNIT = "GNIT"


class SCTR_STATES(models.TextChoices):
    """Allowed coices for SCTR states."""

    draft = "Draft"
    published = "Pubished"
    hidden = "Hidden"


class SOURCE_COMPONENT_TYPE(models.TextChoices):
    """Allowed choices for source component type."""

    externally_sourced = "Externally Sourced"
    made_in_house = "Made In-House"


class Company(models.Model):
    """Company model."""

    # Required fields
    website = models.CharField(
        max_length=255,
        validators=[full_domain_validator],
        unique=True
    )
    name = models.CharField(max_length=200)
    jurisdiction = models.CharField(
        max_length=400,
    )

    # Optional fields
    # This field is needed for future
    company_unique_identifier = models.FileField(
        upload_to="company_identifiers/%Y/%m",
        null=True,
        blank=True
    )

    # Slug field to use in url
    slug = models.SlugField(null=True)

    def set_slug(self):
        """Sets slug from company name."""
        self.slug = slugify(self.name)


class CustomUserManager(BaseUserManager):
    """Administrator model manager."""

    def create_user(self, password, **extra_fields):
        """Overwritten create_user for password encoding."""
        user = self.model(**extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, password, **extra_fields):
        """Overwritten create_superuser for password encoding."""
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        return self.create_user(password, **extra_fields)


class Administrator(AbstractUser):
    """Main user class."""

    # Required fields
    # Password is implemented under the hood
    # As a part of AbstractUser
    email = models.EmailField(max_length=250, unique=True)

    # Optional fields
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)

    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)

    objects = CustomUserManager()

    REQUIRED_FIELDS = []

    # Override (delete) username default field from django.
    username = None
    # Use email as a username (need for authentication)
    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def update_password(self, new_password):
        """Method for encoding the password."""
        self.set_password(new_password)
        self.save()

    def __str__(self):
        """Str magic method for Administrator model."""
        return self.email

    def add_group(self, group):
        """Add user to the group."""
        group, _ = Group.objects.get_or_create(name=group)
        group.user_set.add(self)


class SCTR(models.Model):
    """SCTR model."""

    # According to the public information
    # SKU length is usually not more then 25 characters
    # GNIT length is 13
    unique_identifier = models.CharField(max_length=25, unique=True)
    unique_identifier_type = models.CharField(
        max_length=4,
        choices=SCTR_ID_TYPES.choices
    )
    marketing_name = models.CharField(max_length=500)

    version = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1)
        ]
    )
    state = models.CharField(
        max_length=8,
        choices=SCTR_STATES.choices
    )

    sctr_cogs = models.FloatField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class SourceComponent(models.Model):
    """SCTR source components model."""

    fraction_cogs = models.FloatField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
    )
    marketing_name = models.CharField(max_length=500)
    component_type = models.CharField(
        max_length=18,
        choices=SOURCE_COMPONENT_TYPE.choices
    )

    # On of this fields will be set according to the type
    # This check is applied in the serializer
    country_of_origin = CountryField(null=True)
    external_sku = models.CharField(max_length=25, null=True)

    parent_sctr = models.ForeignKey(SCTR, related_name="components", on_delete=models.CASCADE)
