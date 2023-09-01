# Copyright 2023 Free World Certified -- all rights reserved.
"""API SCTR-related views module."""
from api.filter import SCTRFilter
from api.models import SCTR
from api.models import SCTR_STATES
from api.models import SOURCE_COMPONENT_TYPE
from api.models import SourceComponent
from api.permissions import IsComponentOwner
from api.permissions import IsSCTROwner
from api.permissions import ReadOnly
from api.serializers import SCTRCreateSerializer
from api.serializers import SCTRDraftCreateSerializer
from api.serializers import SCTRGetSerializer
from api.serializers import SCTRPublishValidatorSerializer
from api.serializers import SCTRSerializer
from api.serializers import SourceComponentDraftSerializer
from api.serializers import SourceComponentSerializer
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response


class SCTRCreateView(CreateAPIView):
    """SCTR creation."""

    serializer_class = SCTRCreateSerializer
    permission_classes = [IsAuthenticated, ]


class SCTRCreateDraftView(CreateAPIView):
    """SCTR creation with draft state."""

    serializer_class = SCTRDraftCreateSerializer
    permission_classes = [IsAuthenticated]


class SCTRPublishedListView(ListAPIView):
    """Gets published SCTRs only and provides filtering."""

    serializer_class = SCTRGetSerializer
    queryset = SCTR.objects.filter(state=SCTR_STATES.PUBLISHED)
    filterset_class = SCTRFilter


class SCTRSwitchVisibilityView(UpdateAPIView):
    """Switches SCTR visibility."""

    permission_classes = [IsAuthenticated, IsSCTROwner]
    lookup_field = "unique_identifier"
    queryset = SCTR.objects.exclude(state=SCTR_STATES.DRAFT)

    def update(self, request, unique_identifier):
        """Switches SCTR visibility."""
        sctr = self.get_object()

        if sctr.state == SCTR_STATES.PUBLISHED:
            sctr.state = SCTR_STATES.HIDDEN
        else:
            sctr.state = SCTR_STATES.PUBLISHED
        sctr.save()

        return Response(
            {"message": "Successfuly switch visibility"},
            status=200
        )


class SCTRCompanyListView(ListAPIView):
    """Gets all user's company SCTRs and provides filtering."""

    permission_classes = [IsAuthenticated]
    serializer_class = SCTRGetSerializer
    filterset_class = SCTRFilter

    def get_queryset(self):
        """Gets all SCTRs that are related to the user's company."""
        return SCTR.objects.filter(
            company=self.request.user.company
        )


class SCTRRetrieveDestroyView(RetrieveDestroyAPIView):
    """View has get and delete methods for SCTR model."""

    permission_classes = [IsAuthenticatedOrReadOnly, ReadOnly | IsSCTROwner]
    lookup_field = "unique_identifier"
    serializer_class = SCTRGetSerializer

    def get_queryset(self):
        """Queryset based on user's authentication."""
        # Not authenticated users can access only published produts
        if self.request.user:
            return SCTR.objects.all()
        else:
            return SCTR.objects.filter(state=SCTR_STATES.PUBLISHED)


class SCTRUpdateView(UpdateAPIView):
    """View has patch method for SCTR model."""

    permission_classes = [IsAuthenticated, IsSCTROwner]
    lookup_field = "unique_identifier"
    serializer_class = SCTRSerializer
    queryset = SCTR.objects.filter(state=SCTR_STATES.DRAFT)


class SCTRMoveToDraftView(UpdateAPIView):
    """View for moving SCTR to draft state."""

    permission_classes = [IsAuthenticated, IsSCTROwner]
    lookup_field = "unique_identifier"
    serializer_class = SCTRSerializer
    queryset = SCTR.objects.exclude(state=SCTR_STATES.DRAFT)

    def patch(self, request, unique_identifier):
        """Update instance state."""
        instance = get_object_or_404(SCTR, unique_identifier=unique_identifier)
        instance.state = SCTR_STATES.DRAFT
        instance.save()
        return Response(status=200, data={"message": "Intance was moved to the draft state"})


class SCTRMoveToPublishedView(UpdateAPIView):
    """View for moving SCTR to draft state."""

    permission_classes = [IsAuthenticated, IsSCTROwner]
    lookup_field = "unique_identifier"
    queryset = SCTR.objects.exclude(state=SCTR_STATES.PUBLISHED)

    def patch(self, request, unique_identifier):
        """Moves instance to published state."""
        sctr = get_object_or_404(SCTR, unique_identifier=unique_identifier)
        components = SourceComponent.objects.filter(parent_sctr=sctr).values(
            "marketing_name",
            "fraction_cogs",
            "component_type",
            "external_sku",
            "country_of_origin"
        )

        sctr_serialized = SCTRPublishValidatorSerializer(data=sctr.__dict__)
        if not sctr_serialized.is_valid():
            return Response(status=400, data=sctr_serialized.errors)

        components_serialized = SourceComponentSerializer(data=list(components), many=True)

        if not components_serialized.is_valid():
            return Response(status=400, data=components_serialized.errors)

        if components.aggregate(Sum("fraction_cogs"))["fraction_cogs__sum"] != 100:
            return Response(status=400, data={"message": "COGS should be 100%"})
        sctr.state = SCTR_STATES.PUBLISHED
        sctr.save()
        return Response(status=200, data={"message": "Intance was moved to the published state"})


class ComponentCreateView(CreateAPIView):
    """View for component creation."""

    permission_classes = [IsAuthenticated, IsSCTROwner]
    serializer_class = SourceComponentSerializer

    def post(self, request, unique_identifier):
        """Creates empty component and attaches it to sctr."""
        data = {
            "fraction_cogs": 0,
            "marketing_name": "",
            "component_type": SOURCE_COMPONENT_TYPE.made_in_house,
        }
        sctr = get_object_or_404(SCTR, unique_identifier=unique_identifier)
        component = SourceComponentDraftSerializer(data=data)

        if not component.is_valid():
            return Response(component.errors, status=400)

        component.validated_data["parent_sctr"] = sctr
        component.validated_data["country_of_origin"] = ""
        component.validated_data["external_sku"] = None
        component.save()

        return Response(component.data, status=200)


class ComponentPatchRetrieveDeleteView(RetrieveUpdateDestroyAPIView):
    """Component patch, retrieve and delete view."""

    permission_classes = [IsAuthenticated, IsComponentOwner]
    serializer_class = SourceComponentDraftSerializer
    lookup_field = "id"
    queryset = SourceComponent.objects.all()
