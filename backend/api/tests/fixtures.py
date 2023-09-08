# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains useful fixtures."""
import pytest
from api.tests.factories.factories import AdministratorFactory
from api.tests.factories.factories import CompanyFactory
from api.tests.factories.factories import ComponentFactory
from api.tests.factories.factories import GroupFactory
from django.test import Client
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def sctr():
    """Create component and SCTR."""
    component = ComponentFactory()

    # Returns SCTR that has component
    return component.parent_sctr


@pytest.fixture
def admin():
    """Creates an admin."""
    # Inner function to create fixture with parameters
    def _method(
        email="admin@gmail.com",
        password="1234",
        company=CompanyFactory.create()
    ):
        return AdministratorFactory(
            email=email,
            password=password,
            company=company,
            groups=[GroupFactory(name="Administrator")]
        )

    return _method


@pytest.fixture
def pm():
    """Creates an pm."""
    # Inner function to create fixture with parameters
    def _method(
        email="pmpm@gmail.com",
        password="1234",
        company=CompanyFactory.create()
    ):
        return AdministratorFactory(
            email=email,
            password=password,
            company=company,
            groups=[GroupFactory(name="PM")]
        )

    return _method


@pytest.fixture
def auth_header():
    """Authentication header for a user."""
    # Inner function to create fixture with parameters
    def _method(user):
        access_token = str(AccessToken.for_user(user))
        credentials = {
            "HTTP_AUTHORIZATION": "Bearer " + access_token
        }
        return credentials

    return _method


@pytest.fixture
def sctr_dict():
    """Returns dict with SCTR and components for 'create and publish'."""
    obj = {
        "unique_identifier_type_str": "SKU",
        "unique_identifier": "1aa24a211232aa",
        "marketing_name": "aaaa",
        "components": [
            {
                "fraction_cogs": 99,
                "marketing_name": "why",
                "component_type_str": "EXTERNALLY_SOURCED",
                "external_sku": "aaaaa",
                "country_of_origin": "USA"
            },
            {
                "fraction_cogs": 1,
                "marketing_name": "why1",
                "component_type_str": "MADE_IN_HOUSE",
                "external_sku": "aaaaa1",
                "country_of_origin": "China"
            }
        ]
    }
    return obj


@pytest.fixture
def sctr_invalid_dict():
    """Returns dict with SCTR and components that is invalid for 'create and publish'.

    This data is valid for creating a draft
    """
    obj = {
        "unique_identifier": "1aa24a211232aa",
        "components": [
            {
                "fraction_cogs": 0,
            },
            {
                "marketing_name": "why1",
            }
        ]
    }
    return obj
