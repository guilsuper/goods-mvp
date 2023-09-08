# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains test for the following url names.

sctr-create
sctr-create-draft
"""
import pytest
from api.models import SCTR
from django.urls import reverse


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, sctr_info, status_code, count", [
        # Try to create as unauthorized user without data
        # The user is not allowed to create it
        (None, None, 401, 1),
        # Try to create as unauthorized user with correct data
        # The user is not allowed to create it
        (None, "sctr_dict", 401, 1),
        # Try to create as unauthorized user with incorrect data
        # The user is not allowed to create it
        (None, "sctr_invalid_dict", 401, 1),
        # Try to create as an admin with no specified fields
        # The SCTR won't be created
        ("admin", None, 400, 1),
        # Try to create as an admin with a correct specified fields
        # The SCTR will be created
        ("admin", "sctr_dict", 201, 2),
        # Try to create as an admin with a incorrect specified fields
        # The SCTR will not be created
        ("admin", "sctr_invalid_dict", 400, 1),
        # Try to create as a pm with no specified fields
        # The SCTR won't be created
        ("pm", None, 400, 1),
        # Try to create as a pm with a correct specified fields
        # The SCTR will be created
        ("pm", "sctr_dict", 201, 2),
        # Try to create as a pm with a incorrect specified fields
        # The SCTR will not be created
        ("pm", "sctr_invalid_dict", 400, 1),
    ]
)
def test_sctr_create_and_publish(
    request, client, sctr,
    auth_header, user, sctr_info,
    status_code, count
):
    """Tests sctr-create url."""
    # credentials must be a dict to pass them to the post request
    credentials = dict()
    # If parameter is not empty, replace it with actual data
    if user:
        # user is a fixture with parameters
        user = request.getfixturevalue(user)()
        credentials = auth_header(user)

    # If parameter is not empty, replace it with actual data
    if sctr_info:
        # If sctr_info is not None, it contains string "sctr_dict"
        sctr_info = request.getfixturevalue(sctr_info)

    response = client.post(
        reverse("sctr-create"),
        data=sctr_info,
        content_type="application/json",
        **credentials
    )

    assert response.status_code == status_code
    assert len(SCTR.objects.all()) == count

    # One sctr is created after using a sctr fixture
    # The second is created after user's request
    sctr_created = count == 2

    if sctr_created:
        current_sctr = SCTR.objects.filter(
            unique_identifier=sctr_info["unique_identifier"]
        ).first()

        assert current_sctr.company == user.company
        assert current_sctr.unique_identifier == sctr_info["unique_identifier"]


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, sctr_info, status_code, count", [
        # Try to create as unauthorized user without data
        # The user is not allowed to create it
        (None, None, 401, 1),
        # Try to create as unauthorized user with correct data
        # The user is not allowed to create it
        (None, "sctr_dict", 401, 1),
        # Try to create as unauthorized user with incorrect data
        # The user is not allowed to create it
        (None, "sctr_invalid_dict", 401, 1),
        # Try to create as an admin with no specified fields
        # The sctr won't be created
        ("admin", None, 400, 1),
        # Try to create as an admin with a correct specified fields
        # The sctr will be created
        ("admin", "sctr_dict", 201, 2),
        # Try to create as an admin with a incorrect specified fields
        # The sctr will be created
        ("admin", "sctr_invalid_dict", 201, 2),
        # Try to create as a pm with no specified fields
        # The sctr won't be created
        ("pm", None, 400, 1),
        # Try to create as a pm with a correct specified fields
        # The sctr will be created
        ("pm", "sctr_dict", 201, 2),
        # Try to create as a pm with a incorrect specified fields
        # The sctr will be created
        ("pm", "sctr_invalid_dict", 201, 2),
    ]
)
def test_sctr_create_draft(
    request, client, sctr,
    auth_header, user, sctr_info,
    status_code, count
):
    """Tests sctr-create-draft url."""
    # credentials must be a dict to pass them to the post request
    credentials = dict()
    # If parameter is not empty, replace it with actual data
    if user:
        # user is a fixture with parameters
        user = request.getfixturevalue(user)()
        credentials = auth_header(user)

    # If parameter is not empty, replace it with actual data
    if sctr_info:
        # If sctr_info is not None, it contains string "sctr_invalid_dict"
        sctr_info = request.getfixturevalue(sctr_info)

    response = client.post(
        reverse("sctr-create-draft"),
        data=sctr_info,
        content_type="application/json",
        **credentials
    )

    assert response.status_code == status_code
    assert len(SCTR.objects.all()) == count

    # One sctr is created after using a sctr fixture
    # The second is created after user's request
    sctr_created = count == 2

    if sctr_created:
        current_sctr = SCTR.objects.filter(
            unique_identifier=sctr_info["unique_identifier"]
        ).first()

        assert current_sctr.company == user.company
        assert current_sctr.unique_identifier == sctr_info["unique_identifier"]
