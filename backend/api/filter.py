# Copyright 2023 Free World Certified -- all rights reserved.
"""Module with OriginReportFIlter."""
import django_filters
from api.models import OriginReport


class OriginReportFilter(django_filters.FilterSet):
    """FIlter for OriginReport objects."""

    class Meta:
        """Metaclass of the OriginReportFilter."""

        model = OriginReport
        fields = {
            "unique_identifier": ["icontains"],
            "marketing_name": ["icontains"],

            "cogs": ["gte", "lte"],

            "company__name": ["icontains"]
        }
