"""API views module."""

from api.filter import ProductFilter
from api.models import Administrator, Product
from api.serializers import (
    AdministratorRetrieveSerializer,
    AdministratorSerializer,
    ProductSerializer
)
from api.tokens import account_activation_token
from api.utils import send_activation_email

from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from rest_framework import status
from rest_framework.generics import (
    CreateAPIView, DestroyAPIView,
    ListAPIView, RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class Smoke(ListAPIView):
    """Backend healthcheck."""

    def get(self, request):
        """Retrieving basic response."""
        return Response("Working as intended.")


class ProductCreate(CreateAPIView):
    """Product creation."""

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, ]


class ProductRetrieve(ListAPIView):
    """Product retrieving all and filtering."""

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filterset_class = ProductFilter


class CreateAdministrator(CreateAPIView):
    """Administrator creation."""

    serializer_class = AdministratorSerializer

    def post(self, request, *args, **kwargs):
        """Overwritten post method for Administrator creation."""
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            admin = serializer.save()
            if send_activation_email(
                admin.id,
            ):
                return Response(
                    data=request.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                admin.delete()

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivationView(RetrieveAPIView):
    """Email administrator activation view."""

    serializer_class = AdministratorSerializer

    def get(self, request, uidb64, token):
        """Activation view for activating user accounts."""
        Administrator = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            admin = Administrator.objects.get(id=uid)
        except(
            TypeError, ValueError,
            OverflowError, Administrator.DoesNotExist
        ):
            admin = None

        if admin and account_activation_token.check_token(admin, token):
            admin.is_active = True
            admin.save()
            return Response(
                data={"message": "Activated " + admin.email},
                status=status.HTTP_200_OK
            )

        return Response(
            data={"message": "Activation denied"},
            status=status.HTTP_400_BAD_REQUEST
        )


class PatchAdministrator(UpdateAPIView):
    """Administrator patch view."""

    serializer_class = AdministratorSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = Administrator.objects.all()


class GetUser(ListAPIView):
    """Retrieves the current user."""

    serializer_class = AdministratorRetrieveSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        """Returns serialized request.user."""
        return Response(AdministratorRetrieveSerializer(request.user).data)


class DeleteUser(DestroyAPIView):
    """Deletes the current user."""

    permission_classes = [IsAuthenticated]

    def delete(self, request):
        """Overwritten delete method for Administrators."""
        request.user.delete()

        return Response(
            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
            data={"message": "Successfully deleted"}
        )
