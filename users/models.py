from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_member = models.BooleanField(default=False)
    is_organization = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)