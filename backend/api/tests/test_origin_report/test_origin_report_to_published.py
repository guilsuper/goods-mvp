# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains test for the following url names.

origin-report-to-publish
"""
import pytest
from api.models import ORIGIN_REPORT_STATES
from api.models import OriginReport
from django.urls import reverse


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, status_code, is_same_company, is_correct_origin_report", [
        # Unauthorized users can't use this
        (None, 401, False, True),
        (None, 401, True, True),
        (None, 401, False, False),
        (None, 401, True, False),
        # Admins from the different company can't move to published
        ("admin", 403, False, False),
        ("admin", 403, False, True),
        # Admins from the same company can move OriginReport to published
        # If the data is correct
        ("admin", 200, True, True),
        ("admin", 400, True, False),
        # PMs from the different company can't move to published
        ("pm", 403, False, False),
        ("pm", 403, False, True),
        # PMs from the same company can move OriginReport to published
        # If the data is correct
        ("pm", 200, True, True),
        ("pm", 400, True, False),
    ],
)
def test_origin_report_move_to_publish(
    request, client, origin_report,
    auth_header, user, is_same_company,
    status_code, is_correct_origin_report,
):
    """Tests origin-report-to-published url."""
    # credentials must be a dict to pass them to the post request
    credentials = dict()

    # Set origin_report to Draft state
    origin_report.state = ORIGIN_REPORT_STATES.DRAFT
    origin_report.save()
    # Set incorrect origin_report data
    if not is_correct_origin_report:
        origin_report.short_description = ""
        origin_report.save()

    # If parameter is not empty, replace it with actual data
    if user:
        # user is a fixture with parameters
        if is_same_company:
            user = request.getfixturevalue(user)(company=origin_report.company)
        else:
            user = request.getfixturevalue(user)()
        credentials = auth_header(user)

    response = client.patch(
        reverse("origin-report-to-published", kwargs={"id": origin_report.id}),
        **credentials,
    )

    assert response.status_code == status_code
    if status_code == 200:
        assert OriginReport.objects.get(id=origin_report.id).state \
            == ORIGIN_REPORT_STATES.PUBLISHED
    else:
        assert OriginReport.objects.get(id=origin_report.id).state \
            == ORIGIN_REPORT_STATES.DRAFT
