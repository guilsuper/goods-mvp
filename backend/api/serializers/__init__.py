# Copyright 2023 Free World Certified -- all rights reserved.
"""Contains all the views."""
from api.serializers.company_serializers import CompanyRetrieveSerializer
from api.serializers.company_serializers import CompanySerializer
from api.serializers.country_serializers import CountrySerializer
from api.serializers.sctr_and_coponent_serializers import SCTRCreateGetSerializer
from api.serializers.sctr_and_coponent_serializers import SCTRDraftSerializer
from api.serializers.sctr_and_coponent_serializers import SCTRPublishValidatorSerializer
from api.serializers.sctr_and_coponent_serializers import SourceComponentDraftSerializer
from api.serializers.sctr_and_coponent_serializers import SourceComponentSerializer
from api.serializers.user_serializers import AdministratorSerializer
from api.serializers.user_serializers import GroupSerializer
from api.serializers.user_serializers import PMSerializer


__all__ = [
    "CompanyRetrieveSerializer",
    "CompanySerializer",
    "SCTRCreateGetSerializer",
    "SCTRDraftSerializer",
    "SCTRPublishValidatorSerializer",
    "SourceComponentDraftSerializer",
    "SourceComponentSerializer",
    "AdministratorSerializer",
    "GroupSerializer",
    "PMSerializer",
    "CountrySerializer"
]
