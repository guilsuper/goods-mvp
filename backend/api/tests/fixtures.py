# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains useful fixtures."""
import pytest
from api.tests.factories.factories import AdministratorFactory
from api.tests.factories.factories import CompanyFactory
from api.tests.factories.factories import ComponentFactory
from api.tests.factories.factories import GroupFactory
from api.tests.factories.factories import ORIGIN_REPORT_STATES
from api.tests.factories.factories import OriginReportFactory
from django.test import Client
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def origin_report():
    """Create component and OriginReport with published state."""
    component = ComponentFactory()

    # Returns OriginReport that has component
    return component.parent_origin_report


@pytest.fixture
def origin_report_hidden():
    """Create component and OriginReport with hidden state."""
    origin_report_hidden = OriginReportFactory(state=ORIGIN_REPORT_STATES.HIDDEN)
    component = ComponentFactory(parent_origin_report=origin_report_hidden)

    # Returns OriginReport that has component
    return component.parent_origin_report


@pytest.fixture
def origin_report_draft():
    """Create component and OriginReport with draft state."""
    origin_report_draft = OriginReportFactory(state=ORIGIN_REPORT_STATES.DRAFT)
    component = ComponentFactory(parent_origin_report=origin_report_draft)

    # Returns OriginReport that has component
    return component.parent_origin_report


@pytest.fixture
def admin():
    """Creates an admin."""
    # Inner function to create fixture with parameters
    def _method(
        email="admin@gmail.com",
        password="1234",
        company=CompanyFactory.create(),
    ):
        return AdministratorFactory(
            email=email,
            password=password,
            company=company,
            groups=[GroupFactory(name="Administrator")],
        )

    return _method


@pytest.fixture
def pm():
    """Creates an pm."""
    # Inner function to create fixture with parameters
    def _method(
        email="pmpm@gmail.com",
        password="1234",
        company=CompanyFactory.create(),
    ):
        return AdministratorFactory(
            email=email,
            password=password,
            company=company,
            groups=[GroupFactory(name="PM")],
        )

    return _method


@pytest.fixture
def auth_header():
    """Authentication header for a user."""
    # Inner function to create fixture with parameters
    def _method(user):
        access_token = str(AccessToken.for_user(user))
        credentials = {
            "HTTP_AUTHORIZATION": "Bearer " + access_token,
        }
        return credentials

    return _method


@pytest.fixture
def origin_report_dict():
    """Returns dict with OriginReport and components for 'create and publish'."""
    obj = {
        "unique_identifier_type_str": "SKU",
        "unique_identifier": "1aa24a211232aa",
        "short_description": "aaaa",
        "components": [
            {
                "fraction_cogs": 99,
                "short_description": "why",
                "component_type_str": "EXTERNALLY_SOURCED",
                "external_sku": "aaaaa",
                "country_of_origin": "US",
                "company_name": "Mojang",
            },
            {
                "fraction_cogs": 1,
                "short_description": "why1",
                "component_type_str": "MADE_IN_HOUSE",
                "external_sku": "aaaaa1",
                "country_of_origin": "CH",
                "company_name": "Alabama",
            },
        ],
    }
    return obj


@pytest.fixture
def origin_report_invalid_dict():
    """Returns dict with OriginReport and components that is invalid for 'create and publish'.

    This data is valid for creating a draft
    """
    obj = {
        "unique_identifier": "1aa24a211232aa",
        "components": [
            {
                "fraction_cogs": 0,
            },
            {
                "short_description": "why1",
            },
        ],
    }
    return obj


@pytest.fixture
def company():
    """Creates a company."""
    # Inner function to create fixture with parameters
    def _method():
        company = CompanyFactory()
        company.set_slug()
        company.save()
        return company

    return _method
