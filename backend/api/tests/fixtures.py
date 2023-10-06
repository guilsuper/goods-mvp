# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains useful fixtures."""
from io import BytesIO

import pytest
from api.tests.factories.factories import AdministratorFactory
from api.tests.factories.factories import CompanyFactory
from api.tests.factories.factories import ComponentFactory
from api.tests.factories.factories import GroupFactory
from api.tests.factories.factories import ORIGIN_REPORT_STATES
from api.tests.factories.factories import OriginReportFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from PIL import Image
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
    # Create in-memory image
    image = Image.new("RGB", (100, 100), "white")
    image_io = BytesIO()
    image.save(image_io, "PNG")
    image_io.seek(0)
    image_name = "test_image.png"

    uploaded_image = SimpleUploadedFile(image_name, image_io.read(), content_type="image/png")

    obj = {
        "unique_identifier_type_str": "SKU",
        "unique_identifier": "1aa24a211232aa",
        "short_description": "aaaa",
        "thumbnail": uploaded_image,
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


def dict_to_form_data(data: dict, sep: str = "[{i}]") -> dict:
    """Converts dict data to multipart/form-data friendly dict.

    Args:
        data: raw python dictionary.
        sep: arrays separator (symbol to identify an array-like variable).

    Returns:
        Modified dictionary that supports multipart content-type.

    Examples:
        Converting the following dictionary:

        ```python
        data = {
            "name": "Abro",
            "status": {
                "code": "112",
                "desc": "why",
                "workers": [
                    {
                        "name": "1111"
                    }
                ]
            },
            "notes": ["1", "2"]
        }
        ```

        Using `dict_to_form_data(data)` results in the
        following multipart/form-data friendly dictionary:

        ```python
        {
            'name': 'Abro',
            'status.code': '112',
            'status.desc': 'why',
            'status.workers[0].name': '1111',
            'notes[0]': '1',
            'notes[1]': '2'
        }
        ```
    """
    def inner(input: dict, inner_sep: str, result: dict, previous=None) -> dict:
        """Inner function to transform data as a recursive function."""
        # If inner element is a dictionary
        if isinstance(input, dict):
            if previous == "dict":
                inner_sep += "."
            for key, value in input.items():
                inner(value, inner_sep + key, result, "dict")
        # If inner element is array-like
        elif isinstance(input, (list, tuple)):
            for index, value in enumerate(input):
                inner(value, inner_sep + sep.format(i=index), result)
        else:
            result[inner_sep] = input

        return result

    return inner(data, "", {})


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
