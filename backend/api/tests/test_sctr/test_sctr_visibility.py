# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains test for the following url names.

sctr-switch-visibility
"""
import pytest
from api.models import SCTR
from django.urls import reverse


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, sctr_state, new_state, status_code", [
        # Unhide draft SCTR as unauthorized
        # User is not allowed to access it
        (None, 1, 1, 401),
        # Hide published SCTR as unauthorized
        # User is not allowed to access it
        (None, 2, 2, 401),
        # Unhide hidden SCTR as unauthorized
        # User is not allowed to access it
        (None, 3, 3, 401),
        # Unhide draft SCTR as admin
        # Draft views aren't available for this view
        ("admin", 1, 1, 404),
        # Hide published SCTR as admin
        # SCTR state will be changed
        ("admin", 2, 3, 200),
        # Unhide hidden SCTR as admin
        # SCTR state will be changed
        ("admin", 3, 2, 200),
        # Unhide draft SCTR as PM
        # Draft views aren't available for this view
        ("pm", 1, 1, 404),
        # Hide published SCTR as PM
        # SCTR state will be changed
        ("pm", 2, 3, 200),
        # Unhide hidden SCTR as PM
        # SCTR state will be changed
        ("pm", 3, 2, 200),
    ]
)
def test_sctr_change_visibility_same_company(
    request, client, sctr,
    auth_header, user, sctr_state,
    new_state, status_code
):
    """Tests sctr-switch-visibility url."""
    # credentials must be a dict to pass them to the post request
    credentials = dict()
    # If parameter is not empty, replace it with actual data
    if user:
        # user is a fixture with parameters
        user = request.getfixturevalue(user)(company=sctr.company)
        credentials = auth_header(user)

    sctr.state = sctr_state
    sctr.save()

    response = client.put(
        reverse(
            "sctr-switch-visibility",
            kwargs={
                "id": sctr.id
            }
        ),
        **credentials
    )

    assert response.status_code == status_code
    assert SCTR.objects.get(id=sctr.id).state == new_state


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, sctr_state, new_state, status_code", [
        # Unhide draft SCTR as unauthorized
        # User is not allowed to access it
        (None, 1, 1, 401),
        # Hide published SCTR as unauthorized
        # User is not allowed to access it
        (None, 2, 2, 401),
        # Unhide hidden SCTR as unauthorized
        # User is not allowed to access it
        (None, 3, 3, 401),
        # Unhide draft SCTR as admin
        # Draft views aren't available for this view
        ("admin", 1, 1, 404),
        # Hide published SCTR as admin
        # Action not allowed
        ("admin", 2, 2, 403),
        # Unhide hidden SCTR as admin
        # Action not allowed
        ("admin", 3, 3, 403),
        # Unhide draft SCTR as PM
        # Draft views aren't available for this view
        ("pm", 1, 1, 404),
        # Hide published SCTR as PM
        # Action not allowed
        ("pm", 2, 2, 403),
        # Unhide hidden SCTR as PM
        # Action not allowed
        ("pm", 3, 3, 403),
    ]
)
def test_sctr_change_visibility_different_company(
    request, client, sctr,
    auth_header, user, sctr_state,
    new_state, status_code
):
    """Tests sctr-switch-visibility url."""
    # credentials must be a dict to pass them to the post request
    credentials = dict()
    # If parameter is not empty, replace it with actual data
    if user:
        # user is a fixture with parameters
        user = request.getfixturevalue(user)()
        credentials = auth_header(user)

    sctr.state = sctr_state
    sctr.save()

    response = client.put(
        reverse(
            "sctr-switch-visibility",
            kwargs={
                "id": sctr.id
            }
        ),
        **credentials
    )

    assert response.status_code == status_code
    assert SCTR.objects.get(id=sctr.id).state == new_state
