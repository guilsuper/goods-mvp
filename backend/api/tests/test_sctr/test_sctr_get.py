# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains test for the following url names.

sctr-get
sctr-get-company
sctr-delete-retrieve
"""
import pytest
from api.models import SCTR_STATES
from django.urls import reverse


@pytest.mark.django_db()
def test_sctr_get(client, sctr):
    """Tests sctr-get."""
    # Try to get SCTRs as unauthorized user
    # Returns all visible SCTRs
    response = client.get(reverse("sctr-get"))

    assert response.status_code == 200
    # If response contains one SCTR information
    assert len(response.json()) == 1


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, status_code, is_same_company, count", [
        # Unauthenticated users can't get company's all SCTRs
        (None, 401, True, 0),
        (None, 401, False, 0),
        # Admins in the same company as a SCTR can get SCTRs
        ("admin", 200, True, 1),
        # Admins in not the same company as a SCTR can get SCTRs
        ("admin", 200, False, 0),
        # PMs in the same company as a SCTR can get SCTRs
        ("pm", 200, True, 1),
        # PMs in not the same company as a SCTR can get SCTRs
        ("pm", 200, False, 0)
    ]
)
def test_sctr_get_by_company(
    request, client, auth_header,
    sctr, user, status_code,
    is_same_company, count
):
    """Tests SCTR sctr-get-company."""
    # credentials must be a dict to pass them to the post request
    credentials = dict()
    # If parameter is not empty, replace it with actual data
    if user:
        # user is a fixture with parameters
        if is_same_company:
            user = request.getfixturevalue(user)(company=sctr.company)
        else:
            user = request.getfixturevalue(user)()
        credentials = auth_header(user)

    response = client.get(
        reverse("sctr-get-company"),
        **credentials
    )

    assert response.status_code == status_code
    # If response contains list of SCTRs
    if isinstance(response.json(), list):
        assert len(response.json()) == count


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, status_code, is_same_company, sctr_state", [
        # Unauthenticated users can't get company's all SCTRs
        (None, 404, True, "HIDDEN"),
        (None, 200, False, "PUBLISHED"),
        # Admins in the same company as a SCTR can get SCTRs
        ("admin", 200, True, "HIDDEN"),
        ("admin", 200, True, "PUBLISHED"),
        # Admins in not the same company as a SCTR can get SCTRs
        ("admin", 404, False, "HIDDEN"),
        ("admin", 200, False, "PUBLISHED"),
        # PMs in the same company as a SCTR can get SCTRs
        ("pm", 200, True, "HIDDEN"),
        ("pm", 200, True, "PUBLISHED"),
        # PMs in not the same company as a SCTR can get SCTRs
        ("pm", 404, False, "HIDDEN"),
        ("pm", 200, False, "PUBLISHED"),
    ]
)
def test_sctr_get_single(
    request, client, auth_header,
    sctr, user, status_code,
    is_same_company, sctr_state
):
    """Tests SCTR sctr-delete-retrieve."""
    # credentials must be a dict to pass them to the post request
    credentials = dict()
    # set SCTR state
    sctr.state = SCTR_STATES.integer_from_name(sctr_state)
    sctr.save()
    # If parameter is not empty, replace it with actual data
    if user:
        # user is a fixture with parameters
        if is_same_company:
            user = request.getfixturevalue(user)(company=sctr.company)
        else:
            user = request.getfixturevalue(user)()
        credentials = auth_header(user)

    response = client.get(
        reverse(
            "sctr-delete-retrieve",
            kwargs={"id": sctr.id}
        ),
        **credentials
    )

    assert response.status_code == status_code
