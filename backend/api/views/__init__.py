# Copyright 2023 Free World Certified -- all rights reserved.
"""Contains all the views."""
from api.views.company_views import CompanyUpdateRetrieveView
from api.views.product_views import ComponentCreateView
from api.views.product_views import ComponentPatchRetrieveDeleteView
from api.views.product_views import ProductCompanyListView
from api.views.product_views import ProductCreateDraftView
from api.views.product_views import ProductCreateView
from api.views.product_views import ProductMoveToDraftView
from api.views.product_views import ProductMoveToPublishedView
from api.views.product_views import ProductPublishedListView
from api.views.product_views import ProductRetrieveDestroyView
from api.views.product_views import ProductUpdateView
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
    "ProductCreateDraftView",
    "ProductCreateView",
    "ProductPublishedListView",
    "ProductRetrieveDestroyView",
    "ProductUpdateView",
    "ProductCompanyListView",
    "ProductMoveToDraftView",
    "ProductMoveToPublishedView",
    "Smoke",
    "ActivationView",
    "CreateAdministratorAndCompanyView",
    "CreateAdministratorView",
    "PMCreateView",
    "PMListView",
    "PMRetrieveUpdateDestroyView",
    "SelfRetrieveUpdateDestroyView"
]
