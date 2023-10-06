# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains test for the following url names.

origin-report-create
origin-report-create-draft
"""
import pytest
from api.models import OriginReport
from api.tests.fixtures import dict_to_form_data
from django.urls import reverse


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, origin_report_info, status_code, origin_report_created", [
        # Try to create as unauthorized user without data
        # The user is not allowed to create it
        (None, None, 401, False),
        # Try to create as unauthorized user with correct data
        # The user is not allowed to create it
        (None, "origin_report_dict", 401, False),
        # Try to create as unauthorized user with incorrect data
        # The user is not allowed to create it
        (None, "origin_report_invalid_dict", 401, False),
        # Try to create as an admin with no specified fields
        # The OriginReport won't be created
        ("admin", None, 400, False),
        # Try to create as an admin with a correct specified fields
        # The OriginReport will be created
        ("admin", "origin_report_dict", 201, True),
        # Try to create as an admin with a incorrect specified fields
        # The OriginReport will not be created
        ("admin", "origin_report_invalid_dict", 400, False),
        # Try to create as a pm with no specified fields
        # The OriginReport won't be created
        ("pm", None, 400, False),
        # Try to create as a pm with a correct specified fields
        # The OriginReport will be created
        ("pm", "origin_report_dict", 201, True),
        # Try to create as a pm with a incorrect specified fields
        # The OriginReport will not be created
        ("pm", "origin_report_invalid_dict", 400, False),
    ],
)
def test_origin_report_create_and_publish(
    request, client, origin_report,
    auth_header, user, origin_report_info,
    status_code, origin_report_created,
):
    """Tests origin-report-create url."""
    # credentials must be a dict to pass them to the post request
    credentials = dict()
    # If parameter is not empty, replace it with actual data
    if user:
        # user is a fixture with parameters
        user = request.getfixturevalue(user)()
        credentials = auth_header(user)

    # If parameter is not empty, replace it with actual data
    if origin_report_info:
        # If origin_report_info is not None, it contains string "origin_report_dict"
        origin_report_info = dict_to_form_data(request.getfixturevalue(origin_report_info))

    response = client.post(
        reverse("origin-report-create"),
        data=origin_report_info,
        **credentials,
    )

    assert response.status_code == status_code
    assert len(OriginReport.objects.all()) == 2 if origin_report_created else 1

    if origin_report_created:
        current_origin_report = OriginReport.objects.filter(
            unique_identifier=origin_report_info["unique_identifier"],
        ).first()

        assert current_origin_report.company == user.company
        assert current_origin_report.unique_identifier == origin_report_info["unique_identifier"]


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, origin_report_info, status_code, origin_report_created", [
        # Try to create as unauthorized user without data
        # The user is not allowed to create it
        (None, None, 401, False),
        # Try to create as unauthorized user with correct data
        # The user is not allowed to create it
        (None, "origin_report_dict", 401, False),
        # Try to create as unauthorized user with incorrect data
        # The user is not allowed to create it
        (None, "origin_report_invalid_dict", 401, False),
        # Try to create as an admin with no specified fields
        # The origin_report won't be created
        ("admin", None, 400, False),
        # Try to create as an admin with a correct specified fields
        # The origin_report will be created
        ("admin", "origin_report_dict", 201, True),
        # Try to create as an admin with a incorrect specified fields
        # The origin_report will be created
        ("admin", "origin_report_invalid_dict", 201, True),
        # Try to create as a pm with no specified fields
        # The origin_report won't be created
        ("pm", None, 400, False),
        # Try to create as a pm with a correct specified fields
        # The origin_report will be created
        ("pm", "origin_report_dict", 201, True),
        # Try to create as a pm with a incorrect specified fields
        # The origin_report will be created
        ("pm", "origin_report_invalid_dict", 201, True),
    ],
)
def test_origin_report_create_draft(
    request, client, origin_report,
    auth_header, user, origin_report_info,
    status_code, origin_report_created,
):
    """Tests origin-report-create-draft url."""
    # credentials must be a dict to pass them to the post request
    credentials = dict()
    # If parameter is not empty, replace it with actual data
    if user:
        # user is a fixture with parameters
        user = request.getfixturevalue(user)()
        credentials = auth_header(user)

    # If parameter is not empty, replace it with actual data
    if origin_report_info:
        # If origin_report_info is not None, it contains string "origin_report_invalid_dict"
        origin_report_info = dict_to_form_data(request.getfixturevalue(origin_report_info))

    response = client.post(
        reverse("origin-report-create-draft"),
        data=origin_report_info,
        **credentials,
    )

    assert response.status_code == status_code
    assert len(OriginReport.objects.all()) == 2 if origin_report_created else 1

    if origin_report_created:
        current_origin_report = OriginReport.objects.filter(
            unique_identifier=origin_report_info["unique_identifier"],
        ).first()

        assert current_origin_report.company == user.company
        assert current_origin_report.unique_identifier == origin_report_info["unique_identifier"]
