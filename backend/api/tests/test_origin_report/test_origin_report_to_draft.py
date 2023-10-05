# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains test for the following url names.

origin-report-to-draft
"""
import pytest
from api.models import ORIGIN_REPORT_STATES
from api.models import OriginReport
from django.urls import reverse


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, status_code, is_same_company, draft_created", [
        # Unauthorized users can't use this
        (None, 401, False, False),
        (None, 401, True, False),
        # Admins from the different company can't move to draft
        ("admin", 403, False, False),
        # Admins from the same company can move OriginReport to draft
        # Copy of OriginReport will be created in the draft state
        ("admin", 200, True, True),
        # PMs from the different company can't move to draft
        ("pm", 403, False, False),
        # PMs from the same company can move OriginReport to draft
        # Copy of OriginReport will be created in the draft state
        ("pm", 200, True, True),
    ],
)
def test_origin_report_move_to_draft(
    request, client, origin_report,
    auth_header, user, is_same_company,
    status_code, draft_created,
):
    """Tests origin-report-to-draft url."""
    # credentials must be a dict to pass them to the post request
    credentials = dict()
    # If parameter is not empty, replace it with actual data
    if user:
        # user is a fixture with parameters
        if is_same_company:
            user = request.getfixturevalue(user)(company=origin_report.company)
        else:
            user = request.getfixturevalue(user)()
        credentials = auth_header(user)

    response = client.patch(
        reverse("origin-report-to-draft", kwargs={"id": origin_report.id}),
        **credentials,
    )

    assert response.status_code == status_code
    assert len(OriginReport.objects.all()) == 2 if draft_created else 1

    # If moved to draft
    if draft_created:
        # Check that 2 OriginReports exists with the same identifier
        origin_reports = OriginReport.objects.filter(
            unique_identifier=origin_report.unique_identifier,
        )
        assert len(origin_reports) == 2 if draft_created else 1
        # The version should be changed after moving to published state
        assert abs(origin_reports[1].version - origin_reports[0].version) == 0
        # Check that new origin_report is in draft state
        new_origin_report = [
            origin_report_curr for origin_report_curr in
            origin_reports if origin_report_curr.id != origin_report.id
        ][0]
        assert new_origin_report.state == ORIGIN_REPORT_STATES.DRAFT
        assert origin_report.state == ORIGIN_REPORT_STATES.PUBLISHED
