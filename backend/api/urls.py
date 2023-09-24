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
from api.views import SCTRCompanyListView
from api.views import SCTRCreateDraftView
from api.views import SCTRCreateView
from api.views import SCTRMoveToDraftView
from api.views import SCTRMoveToPublishedView
from api.views import SCTRPublishedListView
from api.views import SCTRRetrieveDestroyView
from api.views import SCTRSwitchVisibilityView
from api.views import SCTRUpdateView
from api.views import SelfRetrieveUpdateDestroyView
from api.views import Smoke
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    path("", Smoke.as_view(), name="smoke"),

    path(
        "sctr/create/",
        SCTRCreateView.as_view(),
        name="sctr-create"
    ),
    path(
        "sctr/create_draft/",
        SCTRCreateDraftView.as_view(),
        name="sctr-create-draft"
    ),
    path("sctr/get/", SCTRPublishedListView.as_view(), name="sctr-get"),
    path("sctr/get_by_company/", SCTRCompanyListView.as_view(), name="sctr-get-company"),
    path(
        "sctr/delete_retrieve/<int:id>/",
        SCTRRetrieveDestroyView.as_view(),
        name="sctr-delete-retrieve"
    ),
    path(
        "sctr/patch/<int:id>/",
        SCTRUpdateView.as_view(),
        name="sctr-patch"
    ),
    path(
        "sctr/to_draft/<int:id>/",
        SCTRMoveToDraftView.as_view(),
        name="sctr-to-draft"
    ),
    path(
        "sctr/to_published/<int:id>/",
        SCTRMoveToPublishedView.as_view(),
        name="sctr-to-published"
    ),
    path(
        "sctr/switch_visibility/<int:id>/",
        SCTRSwitchVisibilityView.as_view(),
        name="sctr-switch-visibility"
    ),

    path(
        "component/create/<int:id>/",
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
        name="company-patch-retrieve"
    ),

    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token-verify"),
]
