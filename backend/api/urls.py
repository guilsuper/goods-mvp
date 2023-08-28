# Copyright 2023 Free World Certified -- all rights reserved.
"""API urls module."""
from api.views import ActivationView
from api.views import CompanyUpdateRetrieveView
from api.views import CreateAdministratorAndCompanyView
from api.views import CreateAdministratorView
from api.views import PMCreateView
from api.views import PMListView
from api.views import PMRetrieveUpdateDestroyView
from api.views import ProductCreateView
from api.views import ProductListView
from api.views import ProductRetrieveUpdateDestroyView
from api.views import SelfRetrieveUpdateDestroyView
from api.views import Smoke
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    path("", Smoke.as_view(), name="smoke"),

    path(
        "product/create/",
        ProductCreateView.as_view(),
        name="product-create"
    ),
    path("product/get/", ProductListView.as_view(), name="product-get"),
    path(
        "product/patch_delete_retrieve/<str:unique_identifier>/",
        ProductRetrieveUpdateDestroyView.as_view(),
        name="product-patch-delete-retrieve"
    ),

    path(
        "admin_and_company/create/",
        CreateAdministratorAndCompanyView.as_view(),
        name="company-admin-create"
    ),
    path(
        "admin/create/",
        CreateAdministratorView.as_view(),
        name="admin-create"
    ),
    path(
        "self/patch_delete_retrieve/",
        SelfRetrieveUpdateDestroyView.as_view(),
        name="self-patch-delete-retrieve"
    ),
    path(
        "activate/<uidb64>/<token>/",
        ActivationView.as_view(),
        name="activate"
    ),

    path("pm/create/", PMCreateView.as_view(), name="pm-create"),
    path("pm/list/", PMListView.as_view(), name="pm-list"),
    path(
        "pm/patch_delete_retrieve/<str:email>/",
        PMRetrieveUpdateDestroyView.as_view(),
        name="pm-patch-delete-retrieve"
    ),

    path(
        "company/patch_retrieve/<slug:slug>/",
        CompanyUpdateRetrieveView.as_view(),
        name="company-patch-retrieve"),

    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token-verify"),
]
