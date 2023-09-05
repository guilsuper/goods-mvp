# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains test for the following url names.

sctr-to-publish
"""
import pytest
from api.models import SCTR
from api.models import SCTR_STATES
from django.urls import reverse


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, status_code, is_same_company, is_correct_sctr", [
        # Unauthorized users can't use this
        (None, 401, False, True),
        (None, 401, True, True),
        (None, 401, False, False),
        (None, 401, True, False),
        # Admins from the different company can't move to published
        ("admin", 403, False, False),
        ("admin", 403, False, True),
        # Admins from the same company can move SCTR to published
        # If the data is correct
        ("admin", 200, True, True),
        ("admin", 400, True, False),
        # PMs from the different company can't move to published
        ("pm", 403, False, False),
        ("pm", 403, False, True),
        # PMs from the same company can move SCTR to published
        # If the data is correct
        ("pm", 200, True, True),
        ("pm", 400, True, False),
    ]
)
def test_sctr_move_to_publish(
    request, client, sctr,
    auth_header, user, is_same_company,
    status_code, is_correct_sctr
):
    """Tests sctr-to-published url."""
    # credentials must be a dict to pass them to the post request
    credentials = dict()

    # Set sctr to Draft state
    sctr.state = SCTR_STATES.integer_from_name("DRAFT")
    sctr.save()
    # Set incorrect sctr data
    if not is_correct_sctr:
        sctr.marketing_name = ""
        sctr.save()

    # If parameter is not empty, replace it with actual data
    if user:
        # user is a fixture with parameters
        if is_same_company:
            user = request.getfixturevalue(user)(company=sctr.company)
        else:
            user = request.getfixturevalue(user)()
        credentials = auth_header(user)

    response = client.patch(
        reverse("sctr-to-published", kwargs={"id": sctr.id}),
        **credentials
    )

    assert response.status_code == status_code
    if status_code == 200:
        assert SCTR.objects.get(id=sctr.id).state == SCTR_STATES.integer_from_name("PUBLISHED")
    else:
        assert SCTR.objects.get(id=sctr.id).state == SCTR_STATES.integer_from_name("DRAFT")
