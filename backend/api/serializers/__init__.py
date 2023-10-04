# Copyright 2023 Free World Certified -- all rights reserved.
"""Contains all the views."""
from api.serializers.company_serializers import CompanyRetrieveSerializer
from api.serializers.company_serializers import CompanySerializer
from api.serializers.country_serializers import CountrySerializer
from api.serializers.origin_report_and_component_serializers import OriginReportCreateGetSerializer
from api.serializers.origin_report_and_component_serializers import OriginReportDraftSerializer
from api.serializers.origin_report_and_component_serializers \
    import OriginReportPublishValidatorSerializer
from api.serializers.origin_report_and_component_serializers import SourceComponentDraftSerializer
from api.serializers.origin_report_and_component_serializers import SourceComponentSerializer
from api.serializers.user_serializers import AdministratorSerializer
from api.serializers.user_serializers import GroupSerializer
from api.serializers.user_serializers import PMSerializer


__all__ = [
    "CompanyRetrieveSerializer",
    "CompanySerializer",
    "OriginReportCreateGetSerializer",
    "OriginReportDraftSerializer",
    "OriginReportPublishValidatorSerializer",
    "SourceComponentDraftSerializer",
    "SourceComponentSerializer",
    "AdministratorSerializer",
    "GroupSerializer",
    "PMSerializer",
    "CountrySerializer"
]
