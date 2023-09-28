# Copyright 2023 Free World Certified -- all rights reserved.
"""Contains all the views."""
from api.views.company_views import CompanyUpdateRetrieveView
from api.views.origin_report_views import ComponentCreateView
from api.views.origin_report_views import ComponentPatchRetrieveDeleteView
from api.views.origin_report_views import OriginReportCompanyListView
from api.views.origin_report_views import OriginReportCreateDraftView
from api.views.origin_report_views import OriginReportCreateView
from api.views.origin_report_views import OriginReportMoveToDraftView
from api.views.origin_report_views import OriginReportMoveToPublishedView
from api.views.origin_report_views import OriginReportPublishedListView
from api.views.origin_report_views import OriginReportRetrieveDestroyView
from api.views.origin_report_views import OriginReportSwitchVisibilityView
from api.views.origin_report_views import OriginReportUpdateView
from api.views.smoke_views import Smoke
from api.views.users_views import ActivationView
from api.views.users_views import CreateAdministratorAndCompanyView
from api.views.users_views import CreateAdministratorView
from api.views.users_views import PMCreateView
from api.views.users_views import PMListView
from api.views.users_views import PMRetrieveUpdateDestroyView
from api.views.users_views import SelfRetrieveUpdateDestroyView


__all__ = [
    "CompanyUpdateRetrieveView",
    "ComponentCreateView",
    "ComponentPatchRetrieveDeleteView",
    "OriginReportCreateDraftView",
    "OriginReportCreateView",
    "OriginReportPublishedListView",
    "OriginReportRetrieveDestroyView",
    "OriginReportSwitchVisibilityView",
    "OriginReportUpdateView",
    "OriginReportCompanyListView",
    "OriginReportMoveToDraftView",
    "OriginReportMoveToPublishedView",
    "Smoke",
    "ActivationView",
    "CreateAdministratorAndCompanyView",
    "CreateAdministratorView",
    "PMCreateView",
    "PMListView",
    "PMRetrieveUpdateDestroyView",
    "SelfRetrieveUpdateDestroyView"
]
