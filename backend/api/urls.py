# Copyright 2023 Free World Certified -- all rights reserved.
"""API urls module."""
from api.views import ActivationView
from api.views import CompanyUpdateRetrieveView
from api.views import ComponentCreateView
from api.views import ComponentPatchRetrieveDeleteView
from api.views import CountryView
from api.views import CreateAdministratorAndCompanyView
from api.views import CreateAdministratorView
from api.views import OriginReportCompanyListView
from api.views import OriginReportCreateDraftView
from api.views import OriginReportCreateView
from api.views import OriginReportMoveToDraftView
from api.views import OriginReportMoveToPublishedView
from api.views import OriginReportPublishedListView
from api.views import OriginReportRetrieveDestroyView
from api.views import OriginReportSwitchVisibilityView
from api.views import OriginReportUpdateView
from api.views import PMCreateView
from api.views import PMListView
from api.views import PMRetrieveUpdateDestroyView
from api.views import SelfRetrieveUpdateDestroyView
from api.views import Smoke
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    path("", Smoke.as_view(), name="smoke"),

    path(
        "origin_report/create/",
        OriginReportCreateView.as_view(),
        name="origin-report-create",
    ),
    path(
        "origin_report/create_draft/",
        OriginReportCreateDraftView.as_view(),
        name="origin-report-create-draft",
    ),
    path("origin_report/get/", OriginReportPublishedListView.as_view(), name="origin-report-get"),
    path(
        "origin_report/get_by_company/",
        OriginReportCompanyListView.as_view(),
        name="origin-report-get-company",
    ),
    path(
        "origin_report/delete_retrieve/<int:id>/",
        OriginReportRetrieveDestroyView.as_view(),
        name="origin-report-delete-retrieve",
    ),
    path(
        "origin_report/patch/<int:id>/",
        OriginReportUpdateView.as_view(),
        name="origin-report-patch",
    ),
    path(
        "origin_report/to_draft/<int:id>/",
        OriginReportMoveToDraftView.as_view(),
        name="origin-report-to-draft",
    ),
    path(
        "origin_report/to_published/<int:id>/",
        OriginReportMoveToPublishedView.as_view(),
        name="origin-report-to-published",
    ),
    path(
        "origin_report/switch_visibility/<int:id>/",
        OriginReportSwitchVisibilityView.as_view(),
        name="origin-report-switch-visibility",
    ),

    path(
        "component/create/<int:id>/",
        ComponentCreateView.as_view(),
        name="component-create",
    ),
    path(
        "component/patch_delete_retrieve/<int:id>/",
        ComponentPatchRetrieveDeleteView.as_view(),
        name="component-patch-retrieve-delete",
    ),

    path(
        "admin_and_company/create/",
        CreateAdministratorAndCompanyView.as_view(),
        name="company-admin-create",
    ),
    path(
        "admin/create/",
        CreateAdministratorView.as_view(),
        name="admin-create",
    ),
    path(
        "self/patch_delete_retrieve/",
        SelfRetrieveUpdateDestroyView.as_view(),
        name="self-patch-delete-retrieve",
    ),
    path(
        "activate/<uidb64>/<token>/",
        ActivationView.as_view(),
        name="activate",
    ),

    path("pm/create/", PMCreateView.as_view(), name="pm-create"),
    path("pm/list/", PMListView.as_view(), name="pm-list"),
    path(
        "pm/patch_delete_retrieve/<str:email>/",
        PMRetrieveUpdateDestroyView.as_view(),
        name="pm-patch-delete-retrieve",
    ),

    path(
        "company/patch_retrieve/<slug:slug>/",
        CompanyUpdateRetrieveView.as_view(),
        name="company-patch-retrieve",
    ),

    path(
        "country/list/",
        CountryView.as_view(),
        name="country-list",
    ),

    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token-verify"),
]
