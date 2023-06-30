from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_member', 'is_organization']


admin.site.register(User, UserAdmin)
