# Copyright 2023 Free World Certified -- all rights reserved.
"""API views module."""
from api.filter import ProductFilter
from api.models import Administrator
from api.models import Company
from api.models import Product
from api.permissions import IsAccountOwner
from api.permissions import IsAdministrator
from api.permissions import IsCompanyAdministrator
from api.permissions import IsProductOwner
from api.permissions import ReadOnly
from api.serializers import AdministratorSerializer
from api.serializers import CompanyRetrieveSerializer
from api.serializers import CompanySerializer
from api.serializers import PMSerializer
from api.serializers import ProductCreateSerializer
from api.serializers import ProductGetSerializer
from api.tokens import account_activation_token
from api.utils import send_activation_email
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.parsers import FormParser
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView


class Smoke(ListAPIView):
    """Backend healthcheck."""

    def get(self, request):
        """Retrieving basic response."""
        return Response("Working as intended.")


class ProductCreateView(CreateAPIView):
    """Product creation."""

    serializer_class = ProductCreateSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, ]


class ProductListView(ListAPIView):
    """Product retrieving all and filtering."""

    serializer_class = ProductGetSerializer
    queryset = Product.objects.all()
    filterset_class = ProductFilter


class ProductRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """View has patch, get and delete methods for product model."""

    permission_classes = [IsAuthenticatedOrReadOnly, ReadOnly | IsProductOwner]
    queryset = Product.objects.all()
    lookup_field = "sku_id"

    def get_serializer_class(self):
        """Set initial serializer based on a request method."""
        if self.request.method == "GET":
            return ProductGetSerializer
        else:
            return ProductCreateSerializer


class CreateAdministratorAndCompanyView(APIView):
    """Administrator and company initial creation."""

    # To accept multipart/form-data in case we use file field
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        """Overwritten post method for Administrator creation."""
        data = request.data
        admin = AdministratorSerializer(data=data)
        company = CompanySerializer(data=data)

        if admin.is_valid() and company.is_valid():
            admin = admin.save()

            if send_activation_email(
                admin.id,
            ):
                company = company.save()

                # set company and save model instance
                admin.company = company

                # add initial user to PM group
                # it is a client's requirement
                admin.add_group("PM")
                admin.save()

                return Response(
                    data=data,
                    status=status.HTTP_201_CREATED
                )
            else:
                admin.delete()
                return Response(
                    {"message": "Email wasn't sent"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        # You need to call is_valid before accessing the errors attribute
        # admin.is_valid() is called every time
        # but if admin.is_valid() is false, company.is_valid() wasn't called
        company.is_valid()

        errors = {**admin.errors, **company.errors}

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class CreateAdministratorView(CreateAPIView):
    """Administrator creation."""

    serializer_class = AdministratorSerializer
    permission_classes = [IsAuthenticated, IsAdministrator]

    def post(self, request, *args, **kwargs):
        """Overwritten post method for Administrator creation."""
        admin = self.get_serializer(data=request.data)

        if admin.is_valid():
            admin = admin.save()
            if send_activation_email(
                admin.id,
            ):
                admin.company = request.user.company

                return Response(
                    data=request.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                admin.delete()

        return Response(admin.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivationView(RetrieveAPIView):
    """Email administrator activation view."""

    serializer_class = AdministratorSerializer

    def get(self, request, uidb64, token):
        """Activation view for activating user accounts."""
        Administrator = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            admin = Administrator.objects.get(id=uid)
        except (
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


class SelfRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """Administrator patch, get and delete view."""

    serializer_class = AdministratorSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdministrator | ReadOnly,
        IsAccountOwner
    ]
    queryset = Administrator.objects.all()

    def patch(self, request):
        """Overwritten patch method for using patch without pk."""
        instance = request.user
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def get(self, request):
        """Returns serialized request.user."""
        self.serializer_class = self.get_serializer_class()
        return Response(
            {
                **self.serializer_class(request.user).data,
            }
        )

    def delete(self, request):
        """Overwritten delete method for Administrators."""
        request.user.delete()

        return Response(
            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
            data={"message": "Successfully deleted"}
        )

    def get_serializer_class(self):
        """Get serializer based on the user group."""
        if self.request.user.groups.filter(
            name="Administrator"
        ).exists():
            return AdministratorSerializer
        else:
            return PMSerializer


class PMCreateView(CreateAPIView):
    """PM creation."""

    permission_classes = [IsAuthenticated, IsAdministrator]
    serializer_class = PMSerializer

    def post(self, request, *args, **kwargs):
        """Overwritten post method for PM creation."""
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            pm = serializer.save()
            if send_activation_email(
                pm.id,
            ):
                pm.company = request.user.company

                return Response(
                    data=request.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                pm.delete()

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PMRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """PM get, patch and delete methods."""

    serializer_class = PMSerializer
    permission_classes = [
        IsAuthenticated,
        IsAdministrator,
        IsCompanyAdministrator
    ]
    queryset = Administrator.objects.filter(groups__name="PM")
    lookup_field = "email"


class PMListView(ListAPIView):
    """Retrieves the PMs."""

    serializer_class = PMSerializer
    permission_classes = (IsAuthenticated, IsAdministrator, )

    def get_queryset(self):
        """Filter the PMs."""
        return Administrator.objects.filter(
            groups__name="PM",
            company=self.request.user.company
        )


class CompanyUpdateRetrieveView(RetrieveUpdateAPIView):
    """Updates or retrieves company information."""

    permission_classes = [
        IsAuthenticated,
        IsAdministrator,
        IsCompanyAdministrator
    ]
    queryset = Company.objects.all()
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CompanyRetrieveSerializer
        return CompanySerializer
