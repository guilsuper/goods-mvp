# Copyright 2023 Free World Certified -- all rights reserved.
"""Admin panel module."""
from api.models import Administrator
from api.models import Company
from api.models import OriginReport
from api.models import SourceComponent
from django.contrib import admin

# Register your models here.
admin.site.register(OriginReport)
admin.site.register(Administrator)
admin.site.register(Company)
admin.site.register(SourceComponent)
