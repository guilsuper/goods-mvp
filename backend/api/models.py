"""Module contains database tables as models."""

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class Product(models.Model):
    """Product model."""

    sku_id = models.IntegerField()
    public_facing_id = models.IntegerField()
    public_facing_name = models.CharField(max_length=500)
    description = models.TextField(max_length=2000)

    sctr_date = models.DateField()
    sctr_cogs = models.FloatField()

    product_input_manufacturer = models.CharField(max_length=200)
    product_input_type = models.CharField(max_length=200)


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

    email = models.EmailField(max_length=150, unique=True)
    phonenumber = PhoneNumberField(null=True)

    company_name = models.CharField(max_length=200, null=True)
    company_address = models.TextField(max_length=1000, null=True)
    industry = models.CharField(max_length=50, null=True)
    company_size = models.IntegerField(null=True)

    objects = CustomUserManager()

    def update_password(self, new_password):
        """Method for encoding the password."""
        self.set_password(new_password)
        self.save()

    def __str__(self):
        """Str magic method for Administrator model."""
        return self.username
