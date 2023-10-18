# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains test for the following url names.

origin-report-patch
"""
from io import BytesIO

import pytest
from api.models import ORIGIN_REPORT_STATES
from api.models import OriginReport
from api.models import SourceComponent
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import BOUNDARY
from django.test.client import encode_multipart
from django.test.client import MULTIPART_CONTENT
from django.urls import reverse
from PIL import Image


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, data, status_code", [
        # Try to update as unauthorized user
        # The user is not allowed to update it
        (None, dict(), 401),
        (None, {"short_description": "aaaaa"}, 401),
        # Try to update a OriginReport as an admin with no specified fields
        # The request will be successful, but without any changes
        ("admin", dict(), 200),
        # Try to update a OriginReport as an admin with specified fields
        # Changes will be applied
        ("admin", {"short_description": "aaaaa"}, 200),
        # Try to update a OriginReport as a PM with no specified fields
        # The request will be successful, but without any changes
        ("pm", dict(), 200),
        # Try to update a OriginReport as a PM with specified fields
        # Changes will be applied
        ("pm", {"short_description": "aaaaa"}, 200),
    ],
)
def test_origin_report_update_same_company(
    request, client, auth_header,
    origin_report, user, data, status_code,
):
    """Tests OriginReport update url with the same user and OriginReport company."""
    # credentials must be a dict to pass them to the post request
    credentials = dict()
    # If parameter is not empty, replace it with actual data
    if user:
        # user is a fixture with parameters
        user = request.getfixturevalue(user)
        user = user(company=origin_report.company)
        credentials = auth_header(user)

    # Move OriginReport to draft, so it is editable
    origin_report.state = ORIGIN_REPORT_STATES.DRAFT
    origin_report.save()

    response = client.patch(
        reverse(
            "origin-report-patch",
            kwargs={"id": origin_report.id},
        ),
        data=data,
        content_type="application/json",
        **credentials,
    )

    assert response.status_code == status_code
    # Ensure data was changed
    if "short_description" in data and user:
        assert OriginReport.objects.get(
            id=origin_report.id,
        ).short_description == data["short_description"]


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, data, status_code", [
        # Try to update as unauthorized user
        # The user is not allowed to update it
        (None, dict(), 401),
        (None, {"short_description": "aaaaa"}, 401),
        # Try to update a OriginReport as an admin with no specified fields
        # The user is not allowed to update it
        ("admin", dict(), 403),
        # Try to update a OriginReport as an admin with specified fields
        # The user is not allowed to update it
        ("admin", {"short_description": "aaaaa"}, 403),
        # Try to update a OriginReport as a PM with no specified fields
        # The user is not allowed to update it
        ("pm", dict(), 403),
        # Try to update a OriginReport as a PM with specified fields
        # The user is not allowed to update it
        ("pm", {"short_description": "aaaaa"}, 403),
    ],
)
def test_origin_report_update_different_company(
    request, client, auth_header,
    origin_report, user, data, status_code,
):
    """Tests OriginReport update url with different user and OriginReport companies."""
    # credentials must be a dict to pass them to the post request
    credentials = dict()
    # If parameter is not empty, replace it with actual data
    if user:
        # user is a fixture with parameters
        user = request.getfixturevalue(user)
        user = user()
        credentials = auth_header(user)

    # Move OriginReport to draft, so it is editable
    origin_report.state = ORIGIN_REPORT_STATES.DRAFT
    origin_report.save()

    response = client.patch(
        reverse(
            "origin-report-patch",
            kwargs={"id": origin_report.id},
        ),
        data=data,
        content_type="application/json",
        **credentials,
    )

    assert response.status_code == status_code
    # If data and user were specified
    # Ensure data wasn't changed
    if "short_description" in data and user:
        assert OriginReport.objects.get(
            id=origin_report.id,
        ).short_description != data["short_description"]


@pytest.mark.django_db()
def test_patch_OR_and_components(
    client, auth_header, admin, origin_report_draft,
):
    admin = admin(company=origin_report_draft.company)
    credentials = auth_header(admin)

    image = Image.new("RGB", (100, 100), "red")
    image_io = BytesIO()
    image.save(image_io, "PNG")
    image_io.seek(0)
    image_name = "test_image.png"

    uploaded_image = SimpleUploadedFile(image_name, image_io.read(), content_type="image/png")

    data = {
        "unique_identifier_type_str": "SKU",
        "unique_identifier": "1aa24a211232aa",
        "short_description": "aaaa",
        "thumbnail": uploaded_image,
        "components": [
            {
                "fraction_cogs": 20,
                "short_description": "why",
                "component_type_str": "EXTERNALLY_SOURCED",
                "external_sku": "aaaaa",
                "country_of_origin": "US",
                "company_name": "Mojang",
            },
            {
                "fraction_cogs": 20,
                "short_description": "why1",
                "component_type_str": "MADE_IN_HOUSE",
                "external_sku": "aaaaa1",
                "country_of_origin": "CH",
                "company_name": "Alabama",
            },
        ],
    }

    response = client.patch(
        reverse(
            "origin-report-patch",
            kwargs={"id": origin_report_draft.id},
        ),
        data=encode_multipart(
            BOUNDARY,
            data,
        ),
        content_type=MULTIPART_CONTENT,
        **credentials,
    )

    assert response.status_code == 200

    components = SourceComponent.objects.filter(parent_origin_report=origin_report_draft)
    assert len(components) == 2
