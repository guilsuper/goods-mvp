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
from api.serializers import SCTRCreateGetSerializer
from api.serializers import SCTRDraftSerializer
from api.serializers import SCTRPublishValidatorSerializer
from api.serializers import SourceComponentDraftSerializer
from api.serializers import SourceComponentSerializer
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response


class SCTRCreateView(CreateAPIView):
    """SCTR creation.

    To create an SCTR instance you need to provide fill all fields.
    """

    serializer_class = SCTRCreateGetSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        """Returns instance with id after creation."""
        instance = serializer.save()

        # Serialize the instance with the id field
        serialized_data = self.serializer_class(instance).data

        return Response(serialized_data, status=status.HTTP_201_CREATED)


class SCTRCreateDraftView(CreateAPIView):
    """SCTR creation with draft state.

    SCTR will have state DRAFT
    Doesn't require all fields to be filled
    """

    serializer_class = SCTRDraftSerializer
    permission_classes = [IsAuthenticated]


class SCTRPublishedListView(ListAPIView):
    """Gets published SCTRs only and provides filtering."""

    serializer_class = SCTRCreateGetSerializer
    queryset = SCTR.objects.filter(state=SCTR_STATES.PUBLISHED)
    filterset_class = SCTRFilter


class SCTRSwitchVisibilityView(UpdateAPIView):
    """Switches SCTR visibility."""

    permission_classes = [IsAuthenticated, IsSCTROwner]
    lookup_field = "id"
    queryset = SCTR.objects.exclude(state=SCTR_STATES.DRAFT)

    def update(self, request, id):
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
    serializer_class = SCTRCreateGetSerializer
    filterset_class = SCTRFilter

    def get_queryset(self):
        """Gets all SCTRs that are related to the user's company."""
        return SCTR.objects.filter(
            company=self.request.user.company
        )


class SCTRRetrieveDestroyView(RetrieveDestroyAPIView):
    """View has get and delete methods for SCTR model."""

    permission_classes = [IsAuthenticatedOrReadOnly, ReadOnly | IsSCTROwner]
    lookup_field = "id"
    serializer_class = SCTRCreateGetSerializer

    def get_queryset(self):
        """Queryset based on user's authentication."""
        # Not authenticated users can access only published SCTRs
        # Authenticated users can acces published and own SCTRs
        published = SCTR.objects.filter(state=SCTR_STATES.PUBLISHED)

        if self.request.user.is_authenticated:
            own = SCTR.objects.filter(company=self.request.user.company)
            return published | own
        else:
            return published


class SCTRUpdateView(UpdateAPIView):
    """View has patch method for SCTR model."""

    permission_classes = [IsAuthenticated, IsSCTROwner]
    lookup_field = "id"
    serializer_class = SCTRDraftSerializer
    queryset = SCTR.objects.filter(state=SCTR_STATES.DRAFT)


class SCTRMoveToDraftView(UpdateAPIView):
    """View for moving SCTR to draft state."""

    permission_classes = [IsAuthenticated, IsSCTROwner]
    lookup_field = "id"
    queryset = SCTR.objects.exclude(state=SCTR_STATES.DRAFT)

    def patch(self, request, id):
        """Creates an instance copy with version += 1 and state = Draft."""
        instance = self.get_object()
        components = SourceComponent.objects.filter(parent_sctr=instance)

        # Makes a copy of the SCTR with diferent version of the same SCTR
        # Also make a copy of each component
        instance.id = None

        instance.version += 1
        instance.state = SCTR_STATES.DRAFT
        instance.save()

        for component in components:
            component.id = None
            component.parent_sctr = instance
            component.save()

        return Response(
            status=200,
            data={"message": "Intance was moved to the draft state"}
        )


class SCTRMoveToPublishedView(UpdateAPIView):
    """View for moving SCTR to publish state."""

    permission_classes = [IsAuthenticated, IsSCTROwner]
    lookup_field = "id"
    queryset = SCTR.objects.exclude(state=SCTR_STATES.PUBLISHED)

    def patch(self, request, id):
        """Validates and moves instance to published state."""
        sctr = self.get_object()
        components = SourceComponent.objects.filter(parent_sctr=sctr).values(
            "marketing_name",
            "fraction_cogs",
            "component_type",
            "external_sku",
            "country_of_origin"
        )

        # Check if COGS is 100
        if components.aggregate(Sum("fraction_cogs"))["fraction_cogs__sum"] != 100:
            return Response(status=400, data={"message": "COGS should be 100%"})

        sctr_serialized = SCTRPublishValidatorSerializer(data=sctr.__dict__)

        if not sctr_serialized.is_valid():
            return Response(status=400, data=sctr_serialized.errors)

        # Transform components to list of dicts
        # And change component_type to component_type_str
        # So the serializer can validate the data
        components = list(components)
        for component in components:
            component["component_type_str"] = \
                SOURCE_COMPONENT_TYPE \
                .name_from_integer(component["component_type"])

        components_serialized = SourceComponentSerializer(data=components, many=True)

        if not components_serialized.is_valid():
            return Response(status=400, data=components_serialized.errors)

        sctr.state = SCTR_STATES.PUBLISHED
        sctr.save()
        return Response(status=200, data={"message": "Intance was moved to the published state"})


class ComponentCreateView(CreateAPIView):
    """View for component creation."""

    permission_classes = [IsAuthenticated, IsSCTROwner]
    serializer_class = SourceComponentSerializer

    def post(self, request, id):
        """Creates empty component and attaches it to sctr."""
        data = {
            "fraction_cogs": 0,
            "marketing_name": "",
            "component_type_str":
                SOURCE_COMPONENT_TYPE.name_from_integer(
                    SOURCE_COMPONENT_TYPE.MADE_IN_HOUSE
                ),
        }
        sctr = get_object_or_404(SCTR, id=id)
        component = SourceComponentDraftSerializer(data=data)

        if not component.is_valid():
            return Response(component.errors, status=400)

        component.validated_data["parent_sctr"] = sctr
        component.validated_data["country_of_origin"] = ""
        component.validated_data["external_sku"] = ""

        component = component.save()
        component = SourceComponentSerializer(component.__dict__)
        return Response(component.data, status=200)


class ComponentPatchRetrieveDeleteView(RetrieveUpdateDestroyAPIView):
    """Component patch, retrieve and delete view."""

    permission_classes = [IsAuthenticated, IsComponentOwner]
    serializer_class = SourceComponentDraftSerializer
    lookup_field = "id"
    queryset = SourceComponent.objects.all()
