# Copyright 2023 Free World Certified -- all rights reserved.
"""API company-related views module."""
from api.models import Company
from api.permissions import IsAdministrator
from api.permissions import IsCompanyAdministrator
from api.serializers import CompanyRetrieveSerializer
from api.serializers import CompanySerializer
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated


class CompanyUpdateRetrieveView(RetrieveUpdateAPIView):
    """Updates or retrieves company information."""

    permission_classes = [
        IsAuthenticated,
        IsAdministrator,
        IsCompanyAdministrator
    ]
    queryset = Company.objects.all()
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CompanyRetrieveSerializer
        return CompanySerializer
