"""Module contains database tables as models."""
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
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
    phonenumber = PhoneNumberField(null=True)

    company_name = models.CharField(max_length=200, null=True)
    company_address = models.TextField(max_length=1000, null=True)
    industry = models.CharField(max_length=50, null=True)
    company_size = models.IntegerField(
        validators=[
            MinValueValidator(1)
        ],
        null=True
    )

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    boss = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)

    objects = CustomUserManager()

    def update_password(self, new_password):
        """Method for encoding the password."""
        self.set_password(new_password)
        self.save()

    def __str__(self):
        """Str magic method for Administrator model."""
        return self.username


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

    owner = models.ForeignKey(Administrator, on_delete=models.CASCADE)


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
