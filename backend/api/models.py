"""Module contains database tables as models."""

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from django_countries.fields import CountryField

from phonenumber_field.modelfields import PhoneNumberField


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


class Company(models.Model):
    """Company model."""

    company_website = models.URLField(max_length=200, unique=True)
    company_name = models.CharField(max_length=200)

    company_jurisdiction = models.CharField(
        max_length=400,
    )
    company_headquarters_physical_address = models.CharField(
        max_length=400,
    )

    # This field is needed for future
    company_unique_identifier = models.FileField(
        upload_to="company_identifiers/%Y/%m",
        null=True
    )

    industry = models.CharField(max_length=50, null=True)
    company_size = models.IntegerField(
        validators=[
            MinValueValidator(1)
        ],
        null=True
    )
    company_phonenumber = PhoneNumberField(null=True)


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

    email = models.EmailField(max_length=250, unique=True)
    phonenumber = PhoneNumberField(null=True, blank=True)

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
        return self.username

    def add_group(self, group):
        """Add user to the group."""
        group, _ = Group.objects.get_or_create(name=group)
        group.user_set.add(self)


class Product(models.Model):
    """Product model."""

    sku_id = models.IntegerField(unique=True)
    public_facing_id = models.IntegerField()
    public_facing_name = models.CharField(max_length=500)
    description = models.TextField(max_length=2000)

    sctr_date = models.DateField()
    sctr_cogs = models.FloatField(
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
    )
    cogs_coutry_recipients = CountryField()

    product_input_manufacturer = models.CharField(max_length=200)
    product_input_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPES.choices
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class SubComponent(models.Model):
    """Product model."""

    sub_sku_id = models.IntegerField()
    sub_public_facing_name = models.CharField(max_length=500, null=True)
    sub_cogs_coutry_recipients = CountryField(null=True)
    sub_product_input_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPES.choices,
        null=True
    )

    main_sku_id = models.ForeignKey(Product, on_delete=models.CASCADE)
