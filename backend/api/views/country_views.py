# Copyright 2023 Free World Certified -- all rights reserved.
"""API country view module."""
from api.models import Country
from api.serializers import CountrySerializer
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView


class CountryView(ListAPIView):
    """Countries."""

    model = Country
    serializer_class = CountrySerializer
    queryset = Country.objects.all()

    filter_backends = [OrderingFilter]
    ordering_fields = "__all__"
    ordering = ["alpha_2"]
