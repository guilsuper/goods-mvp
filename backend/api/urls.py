# Copyright 2023 Free World Certified -- all rights reserved.
"""API urls module."""
from api.views import ActivationView
from api.views import CompanyUpdateRetrieveView
from api.views import ComponentCreateView
from api.views import ComponentPatchRetrieveDeleteView
from api.views import CreateAdministratorAndCompanyView
from api.views import CreateAdministratorView
from api.views import PMCreateView
from api.views import PMListView
from api.views import PMRetrieveUpdateDestroyView
from api.views import ProductCompanyListView
from api.views import ProductCreateDraftView
from api.views import ProductCreateView
from api.views import ProductMoveToDraftView
from api.views import ProductMoveToPublishedView
from api.views import ProductPublishedListView
from api.views import ProductRetrieveDestroyView
from api.views import ProductUpdateView
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
    path(
        "product/create_draft/",
        ProductCreateDraftView.as_view(),
        name="product-create-draft"
    ),
    path("product/get/", ProductPublishedListView.as_view(), name="product-get"),
    path("product/get_by_company/", ProductCompanyListView.as_view(), name="product-get-company"),
    path(
        "product/delete_retrieve/<str:unique_identifier>/",
        ProductRetrieveDestroyView.as_view(),
        name="product-delete-retrieve"
    ),
    path(
        "product/patch/<str:unique_identifier>/",
        ProductUpdateView.as_view(),
        name="product-patch"
    ),
    path(
        "product/to_draft/<str:unique_identifier>/",
        ProductMoveToDraftView.as_view(),
        name="product-to-draft"
    ),
    path(
        "product/to_published/<str:unique_identifier>/",
        ProductMoveToPublishedView.as_view(),
        name="product-to-published"
    ),
    path(
        "component/create/<str:unique_identifier>/",
        ComponentCreateView.as_view(),
        name="component-create"
    ),
    path(
        "component/patch_delete_retrieve/<int:id>/",
        ComponentPatchRetrieveDeleteView.as_view(),
        name="component-patch-retrieve-delete"
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
