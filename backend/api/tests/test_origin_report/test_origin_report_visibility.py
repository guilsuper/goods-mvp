# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains test for the following url names.

origin-report-switch-visibility
"""
import pytest
from api.models import ORIGIN_REPORT_STATES
from api.models import OriginReport
from django.urls import reverse


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, origin_report_state, new_state, status_code", [
        # An unauthenticated user is not allowed to change the view of a OriginReport
        (None, "DRAFT", "DRAFT", 401),
        # An unauthenticated user is not allowed to change the view of a OriginReport
        (None, "PUBLISHED", "PUBLISHED", 401),
        # An unauthenticated user is not allowed to change the view of a OriginReport
        (None, "HIDDEN", "HIDDEN", 401),
        # Unhide draft OriginReport as admin in the same company
        # Draft views aren't available for this view
        ("admin", "DRAFT", "DRAFT", 404),
        # Hide published OriginReport as admin in the same company
        # OriginReport state will be changed
        ("admin", "PUBLISHED", "HIDDEN", 200),
        # Unhide hidden OriginReport as admin in the same company
        # OriginReport state will be changed
        ("admin", "HIDDEN", "PUBLISHED", 200),
        # Unhide draft OriginReport as PM in the same company
        # Draft views aren't available for this view
        ("pm", "DRAFT", "DRAFT", 404),
        # Hide published OriginReport as PM in the same company
        # OriginReport state will be changed
        ("pm", "PUBLISHED", "HIDDEN", 200),
        # Unhide hidden OriginReport as PM in the same company
        # OriginReport state will be changed
        ("pm", "HIDDEN", "PUBLISHED", 200),
    ]
)
def test_origin_report_change_visibility_same_company(
    request, client, origin_report,
    auth_header, user, origin_report_state,
    new_state, status_code
):
    """Tests origin-report-switch-visibility url."""
    # credentials must be a dict to pass them to the post request
    credentials = dict()
    # If parameter is not empty, replace it with actual data
    if user:
        # user is a fixture with parameters
        user = request.getfixturevalue(user)(company=origin_report.company)
        credentials = auth_header(user)

    origin_report.state = ORIGIN_REPORT_STATES.integer_from_name(origin_report_state)
    origin_report.save()

    response = client.put(
        reverse(
            "origin-report-switch-visibility",
            kwargs={
                "id": origin_report.id
            }
        ),
        **credentials
    )

    assert response.status_code == status_code
    assert OriginReport.objects.get(id=origin_report.id).state \
        == ORIGIN_REPORT_STATES.integer_from_name(new_state)


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, origin_report_state, status_code", [
        # An unauthenticated user is not allowed to change the view of a OriginReport
        (None, "DRAFT", 401),
        # An unauthenticated user is not allowed to change the view of a OriginReport
        (None, "PUBLISHED", 401),
        # An unauthenticated user is not allowed to change the view of a OriginReport
        (None, "HIDDEN", 401),
        # Unhide draft OriginReport as admin in a different company
        # Draft views aren't available for this view
        ("admin", "DRAFT", 404),
        # Hide published OriginReport as admin in a different company
        # Action not allowed
        ("admin", "PUBLISHED", 403),
        # Unhide hidden OriginReport as admin in a different company
        # Action not allowed
        ("admin", "HIDDEN", 403),
        # Unhide draft OriginReport as PM in a different company
        # Draft views aren't available for this view
        ("pm", "DRAFT", 404),
        # Hide published OriginReport as PM in a different company
        # Action not allowed
        ("pm", "PUBLISHED", 403),
        # Unhide hidden OriginReport as PM in a different company
        # Action not allowed
        ("pm", "HIDDEN", 403),
    ]
)
def test_origin_report_change_visibility_different_company(
    request, client, origin_report,
    auth_header, user,
    origin_report_state, status_code
):
    """Tests origin-report-switch-visibility url."""
    # credentials must be a dict to pass them to the post request
    credentials = dict()
    # If parameter is not empty, replace it with actual data
    if user:
        # user is a fixture with parameters
        user = request.getfixturevalue(user)()
        credentials = auth_header(user)

    origin_report.state = ORIGIN_REPORT_STATES.integer_from_name(origin_report_state)
    origin_report.save()

    response = client.put(
        reverse(
            "origin-report-switch-visibility",
            kwargs={
                "id": origin_report.id
            }
        ),
        **credentials
    )

    assert response.status_code == status_code
    assert OriginReport.objects.get(id=origin_report.id).state \
        == ORIGIN_REPORT_STATES.integer_from_name(origin_report_state)
