# Copyright 2023 Free World Certified -- all rights reserved.
"""Module with SCTRFIlter."""
import django_filters
from api.models import SCTR


class SCTRFilter(django_filters.FilterSet):
    """FIlter for SCTR objects."""

    class Meta:
        """Metaclas of the SCTRFilter."""

        model = SCTR
        fields = {
            "unique_identifier": ["icontains"],
            "marketing_name": ["icontains"],

            "cogs": ["gte", "lte"],

            "company__name": ["icontains"]
        }
