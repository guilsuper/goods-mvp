# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains test for the following url names.

origin-report-get
origin-report-get-company
origin-report-delete-retrieve
"""
import pytest
from api.models import ORIGIN_REPORT_STATES
from api.models import OriginReport
from django.urls import reverse


@pytest.mark.django_db()
def test_origin_report_get(client, origin_report, origin_report_hidden, origin_report_draft):
    """Tests origin-report-get."""
    # Try to get OriginReports as unauthorized user
    # Returns all visible OriginReports
    response = client.get(reverse("origin-report-get"))

    assert response.status_code == 200
    # Check if OriginReports were initialized
    assert len(OriginReport.objects.all()) == 3
    # If response contains one OriginReport information
    if isinstance(response.json(), list):
        assert len(response.json()) == 1
        assert response.json()[0]["unique_identifier"] == origin_report.unique_identifier


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, status_code, is_same_company, count", [
        # Unauthenticated users can't get companie's OriginReports
        (None, 401, True, 0),
        (None, 401, False, 0),
        # Admins in the same company as a OriginReport can get companie's OriginReports
        ("admin", 200, True, 1),
        # Admins in not the same company as a OriginReport can get companie's OriginReports
        ("admin", 200, False, 0),
        # PMs in the same company as a OriginReport can get companie's OriginReports
        ("pm", 200, True, 1),
        # PMs in not the same company as a OriginReport can get companie's OriginReports
        ("pm", 200, False, 0)
    ]
)
def test_origin_report_get_by_company(
    request, client, auth_header,
    origin_report, user, status_code,
    is_same_company, count
):
    """Tests OriginReport origin-report-get-company."""
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

    response = client.get(
        reverse("origin-report-get-company"),
        **credentials
    )

    assert response.status_code == status_code
    # If response contains list of OriginReports
    if isinstance(response.json(), list):
        assert len(response.json()) == count
        # If count not 0
        if count:
            assert response.json()[0]["unique_identifier"] == origin_report.unique_identifier


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, status_code, is_same_company, origin_report_state", [
        # Unauthenticated users can get only published OriginReports
        (None, 404, True, "HIDDEN"),
        (None, 404, True, "DRAFT"),
        (None, 200, False, "PUBLISHED"),
        # Admins in the same company as a OriginReport can get all the OriginReports
        # can get OriginReports despide its state
        ("admin", 200, True, "HIDDEN"),
        ("admin", 200, True, "DRAFT"),
        ("admin", 200, True, "PUBLISHED"),
        # Admins in not the same company as a OriginReport
        # can get OriginReports that are published only
        ("admin", 404, False, "HIDDEN"),
        ("admin", 404, False, "DRAFT"),
        ("admin", 200, False, "PUBLISHED"),
        # PMs in the same company as a OriginReport
        # can get OriginReports despide its state
        ("pm", 200, True, "HIDDEN"),
        ("pm", 200, True, "DRAFT"),
        ("pm", 200, True, "PUBLISHED"),
        # PMs in not the same company as a OriginReport
        # can get OriginReports that are published only
        ("pm", 404, False, "HIDDEN"),
        ("pm", 404, False, "DRAFT"),
        ("pm", 200, False, "PUBLISHED"),
    ]
)
def test_origin_report_get_single(
    request, client, auth_header,
    origin_report, user, status_code,
    is_same_company, origin_report_state
):
    """Tests OriginReport origin-report-delete-retrieve."""
    # credentials must be a dict to pass them to the post request
    credentials = dict()
    # set OriginReport state
    origin_report.state = ORIGIN_REPORT_STATES.integer_from_name(origin_report_state)
    origin_report.save()
    # If parameter is not empty, replace it with actual data
    if user:
        # user is a fixture with parameters
        if is_same_company:
            user = request.getfixturevalue(user)(company=origin_report.company)
        else:
            user = request.getfixturevalue(user)()
        credentials = auth_header(user)

    response = client.get(
        reverse(
            "origin-report-delete-retrieve",
            kwargs={"id": origin_report.id}
        ),
        **credentials
    )

    assert response.status_code == status_code
    if status_code == 200:
        assert response.json()["unique_identifier"] == origin_report.unique_identifier
