"""API urls module."""

from api.views import (
    ActivationView,
    CreateAdministratorAndCompanyView,
    CreateAdministratorView,
    PMCreateView,
    PMListView,
    PMRetrieveUpdateDestroyView,
    ProductCreateView,
    ProductListView,
    ProductRetrieveUpdateDestroyView,
    SelfRetrieveUpdateDestroyView,
    Smoke,
)

from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    path("", Smoke.as_view(), name="smoke"),

    path(
        "product/create/",
        ProductCreateView.as_view(),
        name="product-create"
    ),
    path("product/get/", ProductListView.as_view(), name="product-get"),
    path(
        "product/patch_delete_retrieve/<int:sku_id>/",
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

    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token-verify"),
]
