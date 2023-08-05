"""API urls module."""

from api.views import (
    ActivationView,
    CreateAdministrator,
    DeleteUser, GetUser,
    PatchAdministrator,
    ProductCreate,
    ProductRetrieve,
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
    path("product/", ProductCreate.as_view(), name="product"),
    path("product/get/", ProductRetrieve.as_view(), name="product-get"),
    path("create_admin/", CreateAdministrator.as_view(), name="create-admin"),
    path("get_current_user/", GetUser.as_view(), name="get-current-user"),
    path(
        "delete_current_user/",
        DeleteUser.as_view(),
        name="delete-current-user"
    ),

    path(
        "patch_admin/<int:pk>",
        PatchAdministrator.as_view(),
        name="patch-current-user"
    ),
    path(
        "activate/<uidb64>/<token>",
        ActivationView.as_view(),
        name="activate"
    ),

    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
