# Copyright 2023 Free World Certified -- all rights reserved.
"""Contains all the views."""
from api.views.company_views import CompanyUpdateRetrieveView
from api.views.country_views import CountryView
from api.views.sctr_views import ComponentCreateView
from api.views.sctr_views import ComponentPatchRetrieveDeleteView
from api.views.sctr_views import SCTRCompanyListView
from api.views.sctr_views import SCTRCreateDraftView
from api.views.sctr_views import SCTRCreateView
from api.views.sctr_views import SCTRMoveToDraftView
from api.views.sctr_views import SCTRMoveToPublishedView
from api.views.sctr_views import SCTRPublishedListView
from api.views.sctr_views import SCTRRetrieveDestroyView
from api.views.sctr_views import SCTRSwitchVisibilityView
from api.views.sctr_views import SCTRUpdateView
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
    "SCTRCreateDraftView",
    "SCTRCreateView",
    "SCTRPublishedListView",
    "SCTRRetrieveDestroyView",
    "SCTRSwitchVisibilityView",
    "SCTRUpdateView",
    "SCTRCompanyListView",
    "SCTRMoveToDraftView",
    "SCTRMoveToPublishedView",
    "Smoke",
    "ActivationView",
    "CreateAdministratorAndCompanyView",
    "CreateAdministratorView",
    "PMCreateView",
    "PMListView",
    "PMRetrieveUpdateDestroyView",
    "SelfRetrieveUpdateDestroyView",
    "CountryView"
]
