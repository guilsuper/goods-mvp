# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains database tables as models."""
from enum import IntEnum

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.core.validators import MinValueValidator
from django.core.validators import RegexValidator
from django.db import models
from django.template.defaultfilters import slugify


full_domain_validator = RegexValidator(
    r"[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9](?:\.[a-zA-Z]{2,})+",
    "Invalid domain, it should be like example.com.eu or example.com"
)


class ChoicesEnum(IntEnum):
    """Base class for choices."""

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def integer_from_name(cls, name):
        """Get the integer of the attribute based on its name."""
        try:
            return cls[name].value
        except KeyError:
            return None

    @classmethod
    def name_from_integer(cls, value):
        """Get the name of the attribute based on its integer value."""
        for key in cls:
            if key.value == value:
                return key.name
        return None


class ORIGIN_REPORT_ID_TYPES(ChoicesEnum):
    """Allowed choices for OriginReport unique identifier types."""
    SKU = 1
    GNIT = 2


class ORIGIN_REPORT_STATES(ChoicesEnum):
    """Allowed choices for OriginReport states."""

    DRAFT = 1
    PUBLISHED = 2
    HIDDEN = 3


class SOURCE_COMPONENT_TYPE(ChoicesEnum):
    """Allowed choices for source component type."""

    EXTERNALLY_SOURCED = 1
    MADE_IN_HOUSE = 2


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


class OriginReport(models.Model):
    """OriginReport model."""

    # According to the public information
    # SKU length is usually not more then 25 characters
    # GNIT length is 13
    unique_identifier = models.CharField(max_length=25)
    unique_identifier_type = models.IntegerField(
        choices=ORIGIN_REPORT_ID_TYPES.choices(),
        default=ORIGIN_REPORT_ID_TYPES.SKU
    )
    marketing_name = models.CharField(
        max_length=500,
        null=True)

    version = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )
    state = models.IntegerField(
        default=ORIGIN_REPORT_STATES.DRAFT,
        choices=ORIGIN_REPORT_STATES.choices()
    )

    cogs = models.FloatField(
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )

    is_latest_version = models.BooleanField(default=False)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Country(models.Model):
    """Country."""

    alpha_2 = models.CharField(max_length=2, primary_key=True)
    alpha_3 = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=255, unique=True)
    free = models.BooleanField(null=False)


class SourceComponent(models.Model):
    """OriginReport source components model."""

    fraction_cogs = models.FloatField(
        blank=True,
        null=True
    )
    marketing_name = models.CharField(max_length=500, null=True, blank=True)
    component_type = models.IntegerField(
        choices=SOURCE_COMPONENT_TYPE.choices(),
        null=True
    )

    # On of this fields will be set according to the type
    # This check is applied in the serializer
    country_of_origin = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    external_sku = models.CharField(max_length=25, null=True)

    # If externally sourced, should store company name
    # The company name should be as a string,
    # in case it isn't in our DB and should be saved
    company_name = models.CharField(max_length=200, null=True)

    parent_origin_report = models.ForeignKey(OriginReport,
                                             related_name="components",
                                             on_delete=models.CASCADE)
