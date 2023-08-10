"""Admin panel module."""
from api.models import Administrator
from api.models import Product
from django.contrib import admin

# Register your models here.
admin.site.register(Product)
admin.site.register(Administrator)
