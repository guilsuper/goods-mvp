# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains test for the following url names.

sctr-to-draft
"""
import pytest
from api.models import SCTR
from django.urls import reverse


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, status_code, is_same_company, count", [
        # Unauthorized users can't use this
        (None, 401, False, 1),
        (None, 401, True, 1),
        # Admins from the different company can't move to draft
        ("admin", 403, False, 1),
        # Admins from the same company can move SCTR to draft
        # Copy of SCTR will be created in the draft state
        ("admin", 200, True, 2),
        # PMs from the different company can't move to draft
        ("pm", 403, False, 1),
        # PMs from the same company can move SCTR to draft
        # Copy of SCTR will be created in the draft state
        ("pm", 200, True, 2),
    ]
)
def test_sctr_move_to_draft(
    request, client, sctr,
    auth_header, user, is_same_company,
    status_code, count
):
    """Tests sctr-to-draft url."""
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

    response = client.patch(
        reverse("sctr-to-draft", kwargs={"id": sctr.id}),
        **credentials
    )

    assert response.status_code == status_code
    assert len(SCTR.objects.all()) == count
