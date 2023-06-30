from django.contrib import admin

from .models import (
    Organization,
    Member,
    Product,
)

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'created_date']

class MemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'address', 'created_date']

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Product)