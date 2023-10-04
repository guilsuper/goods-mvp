# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains test for the following url names.

origin-report-patch
"""
import pytest
from api.models import ORIGIN_REPORT_STATES
from api.models import OriginReport
from django.urls import reverse


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
        ("pm", {"short_description": "aaaaa"}, 200)
    ]
)
def test_origin_report_update_same_company(
    request, client, auth_header,
    origin_report, user, data, status_code
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
            kwargs={"id": origin_report.id}
        ),
        data=data,
        content_type="application/json",
        **credentials
    )

    assert response.status_code == status_code
    # Ensure data was changed
    if "short_description" in data and user:
        assert OriginReport.objects.get(
            id=origin_report.id
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
        ("pm", {"short_description": "aaaaa"}, 403)
    ]
)
def test_origin_report_update_different_company(
    request, client, auth_header,
    origin_report, user, data, status_code
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
            kwargs={"id": origin_report.id}
        ),
        data=data,
        content_type="application/json",
        **credentials
    )

    assert response.status_code == status_code
    # If data and user were specified
    # Ensure data wasn't changed
    if "short_description" in data and user:
        assert OriginReport.objects.get(
            id=origin_report.id
        ).short_description != data["short_description"]
