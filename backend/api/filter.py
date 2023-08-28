# Copyright 2023 Free World Certified -- all rights reserved.
"""Module with ProductFIlter."""
import django_filters
from api.models import SCTR


class ProductFilter(django_filters.FilterSet):
    """FIlter for Product objects."""

    class Meta:
        """Metaclas of the ProductFilter."""

        model = SCTR
        fields = {
            "unique_identifier": ["icontains"],
            "marketing_name": ["icontains"],

            "sctr_cogs": ["gte", "lte"],

            "company__name": ["icontains"]
        }
