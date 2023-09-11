# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains test for the following url names.

sctr-to-draft
"""
import pytest
from api.models import SCTR
from api.models import SCTR_STATES
from django.urls import reverse


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, status_code, is_same_company, draft_created", [
        # Unauthorized users can't use this
        (None, 401, False, False),
        (None, 401, True, False),
        # Admins from the different company can't move to draft
        ("admin", 403, False, False),
        # Admins from the same company can move SCTR to draft
        # Copy of SCTR will be created in the draft state
        ("admin", 200, True, True),
        # PMs from the different company can't move to draft
        ("pm", 403, False, False),
        # PMs from the same company can move SCTR to draft
        # Copy of SCTR will be created in the draft state
        ("pm", 200, True, True),
    ]
)
def test_sctr_move_to_draft(
    request, client, sctr,
    auth_header, user, is_same_company,
    status_code, draft_created
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
    assert len(SCTR.objects.all()) == 2 if draft_created else 1

    # If moved to draft
    if draft_created:
        # Check that 2 SCTRs exists with the same identifier
        sctrs = SCTR.objects.filter(unique_identifier=sctr.unique_identifier)
        assert len(sctrs) == 2 if draft_created else 1
        # The version should be changed after moving to published state
        assert abs(sctrs[1].version - sctrs[0].version) == 0
        # Check that new sctr is in draft state
        new_sctr = [sctr_curr for sctr_curr in sctrs if sctr_curr.id != sctr.id][0]
        assert new_sctr.state == SCTR_STATES.DRAFT
        assert sctr.state == SCTR_STATES.PUBLISHED
