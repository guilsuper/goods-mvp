# Copyright 2023 Free World Certified -- all rights reserved.
"""API OriginReport-related views module."""
from api.filter import OriginReportFilter
from api.models import ORIGIN_REPORT_STATES
from api.models import OriginReport
from api.models import SOURCE_COMPONENT_TYPE
from api.models import SourceComponent
from api.permissions import IsOriginReportOwner
from api.permissions import ReadOnly
from api.serializers import OriginReportCreateGetSerializer
from api.serializers import OriginReportDraftSerializer
from api.serializers import OriginReportPublishValidatorSerializer
from api.serializers import SourceComponentSerializer
from django.db.models import Sum
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response


class OriginReportCreateView(CreateAPIView):
    """OriginReport creation.

    To create an OriginReport instance you need to provide fill all fields.
    """

    serializer_class = OriginReportCreateGetSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Returns instance with id after creation."""
        instance = serializer.save()

        # Serialize the instance with the id field
        serialized_data = self.serializer_class(instance).data

        return Response(serialized_data, status=status.HTTP_201_CREATED)


class OriginReportCreateDraftView(CreateAPIView):
    """OriginReport creation with draft state.

    OriginReport will have state DRAFT
    Doesn't require all fields to be filled
    """

    serializer_class = OriginReportDraftSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Returns instance with id after creation."""
        instance = serializer.save()

        # Serialize the instance with the id field
        serialized_data = self.serializer_class(instance).data

        return Response(serialized_data, status=status.HTTP_201_CREATED)


class OriginReportPublishedListView(ListAPIView):
    """Gets published OriginReports only and provides filtering."""

    serializer_class = OriginReportCreateGetSerializer
    queryset = OriginReport.objects.filter(
        state=ORIGIN_REPORT_STATES.PUBLISHED,
        is_latest_version=True,
    )
    filterset_class = OriginReportFilter


class OriginReportSwitchVisibilityView(UpdateAPIView):
    """Switches OriginReport visibility."""

    permission_classes = [IsAuthenticated, IsOriginReportOwner]
    lookup_field = "id"
    queryset = OriginReport.objects.exclude(state=ORIGIN_REPORT_STATES.DRAFT)

    def update(self, request, id):
        """Switches OriginReport visibility."""
        origin_report = self.get_object()

        if origin_report.state == ORIGIN_REPORT_STATES.PUBLISHED:
            # Should set a is_latest_version to another OriginReport
            # Get previous version if exists
            previous = OriginReport.objects.filter(
                unique_identifier=origin_report.unique_identifier,
                state=ORIGIN_REPORT_STATES.PUBLISHED,
            ).order_by("-version")
            # If has published OriginReports set last as latest version
            if len(previous) > 1:
                instance = previous[1]
                instance.is_latest_version = True
                instance.save()

            origin_report.state = ORIGIN_REPORT_STATES.HIDDEN
            origin_report.is_latest_version = False
        else:
            # is_latest_version should be updated in current OriginReport
            current = OriginReport.objects.filter(
                unique_identifier=origin_report.unique_identifier,
                state=ORIGIN_REPORT_STATES.PUBLISHED,
            ).order_by("-version")
            if current:
                if origin_report.version > current[0].version:
                    origin_report.is_latest_version = True
                    current[0].is_latest_version = False
                    current[0].save()
            origin_report.state = ORIGIN_REPORT_STATES.PUBLISHED
        origin_report.save()

        return Response(
            {"message": "Successfully switch visibility"},
            status=200,
        )


class OriginReportCompanyListView(ListAPIView):
    """Gets all user's company OriginReports and provides filtering."""

    permission_classes = [IsAuthenticated]
    serializer_class = OriginReportCreateGetSerializer
    filterset_class = OriginReportFilter

    def get_queryset(self):
        """Gets all OriginReports that are related to the user's company."""
        return OriginReport.objects.filter(
            company=self.request.user.company,
        )


class OriginReportRetrieveDestroyView(RetrieveDestroyAPIView):
    """View has get and delete methods for OriginReport model."""

    permission_classes = [IsAuthenticatedOrReadOnly, ReadOnly | IsOriginReportOwner]
    lookup_field = "id"
    serializer_class = OriginReportCreateGetSerializer

    def delete(self, request, id):
        instance = self.get_object()
        # Only published OriginReport can have this as True
        if instance.is_latest_version:
            new_latest = OriginReport.objects.filter(
                unique_identifier=instance.unique_identifier,
                state=ORIGIN_REPORT_STATES.PUBLISHED,
            ).order_by("-version")
            # If more then 1 published or hidden origin_reports
            if len(new_latest) > 1:
                obj = new_latest[1]
                obj.is_latest_version = True
                obj.save()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        """Queryset based on user's authentication."""
        # Not authenticated users can access only published OriginReports
        # Authenticated users can access published and own OriginReports
        published = OriginReport.objects.filter(state=ORIGIN_REPORT_STATES.PUBLISHED)

        if self.request.user.is_authenticated:
            own = OriginReport.objects.filter(company=self.request.user.company)
            return published | own
        else:
            return published


class OriginReportUpdateView(UpdateAPIView):
    """View has patch method for OriginReport model."""

    permission_classes = [IsAuthenticated, IsOriginReportOwner]
    lookup_field = "id"
    serializer_class = OriginReportDraftSerializer
    queryset = OriginReport.objects.filter(state=ORIGIN_REPORT_STATES.DRAFT)


class OriginReportMoveToDraftView(UpdateAPIView):
    """View for moving OriginReport to draft state."""

    permission_classes = [IsAuthenticated, IsOriginReportOwner]
    lookup_field = "id"
    queryset = OriginReport.objects.exclude(state=ORIGIN_REPORT_STATES.DRAFT)

    def patch(self, request, id):
        """Creates an instance copy with version += 1 and state = Draft."""
        instance = self.get_object()
        components = SourceComponent.objects.filter(parent_origin_report=instance)

        # Makes a copy of the OriginReport with different version of the same OriginReport
        # Also make a copy of each component
        instance.id = None

        # Not yet published, so it doesn't have the latest version
        # This will be changed when draft is moved to published state
        instance.is_latest_version = False
        instance.state = ORIGIN_REPORT_STATES.DRAFT
        instance.save()

        for component in components:
            component.id = None
            component.parent_origin_report = instance
            component.save()

        return Response(
            status=200,
            data={"message": "Instance was moved to the draft state"},
        )


class OriginReportMoveToPublishedView(UpdateAPIView):
    """View for moving OriginReport to publish state."""

    permission_classes = [IsAuthenticated, IsOriginReportOwner]
    lookup_field = "id"
    queryset = OriginReport.objects.exclude(state=ORIGIN_REPORT_STATES.PUBLISHED)

    def patch(self, request, id):
        """Validates and moves instance to published state."""
        origin_report = self.get_object()
        components = SourceComponent.objects.filter(parent_origin_report=origin_report).values(
            "short_description",
            "fraction_cogs",
            "component_type",
            "external_sku",
            "country_of_origin",
            "company_name",
        )

        # Check if COGS is 100
        if components.aggregate(Sum("fraction_cogs"))["fraction_cogs__sum"] != 100:
            return Response(status=400, data={"message": "COGS should be 100%"})

        origin_report_serialized = \
            OriginReportPublishValidatorSerializer(data=origin_report.__dict__)

        if not origin_report_serialized.is_valid():
            return Response(status=400, data=origin_report_serialized.errors)

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

        # Set previous OriginReport is_latest_version to False
        # If it exists, it's only 1 instance
        old_origin_report = OriginReport.objects.filter(
            unique_identifier=origin_report.unique_identifier,
            is_latest_version=True,
        )
        if old_origin_report:
            old_origin_report[0].is_latest_version = False
            old_origin_report[0].save()

        origin_report.state = ORIGIN_REPORT_STATES.PUBLISHED
        origin_report.is_latest_version = True
        # Real latest version number is in OriginReport that are published or hidden
        old_origin_report = OriginReport.objects.filter(
            unique_identifier=origin_report.unique_identifier,
            state__in=[ORIGIN_REPORT_STATES.PUBLISHED, ORIGIN_REPORT_STATES.HIDDEN],
        ).order_by("-version")
        # If found -- version is changed according to old_origin_report with the highest version
        if old_origin_report:
            origin_report.version = old_origin_report[0].version + 1
        else:
            origin_report.version += 1

        origin_report.save()
        return Response(status=200, data={"message": "Instance was moved to the published state"})
