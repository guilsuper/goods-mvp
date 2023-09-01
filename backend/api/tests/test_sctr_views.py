# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains test for the following url names.

sctr-create, sctr-get
sctr-patch
"""
import pytest
from api.models import SCTR
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

    # Try to get company SCTRs as unauthorized user
    # User can't do that
    response = client.get(reverse("sctr-get-company"))

    assert response.status_code == 401


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, sctr_info, status_code, count", [
        # Try to create as unauthorized user
        # The user is not allowed to create it
        (None, None, 401, 1),
        # Try to create as an admin with no specified fields
        # The SCTR won't be created
        ("admin", None, 400, 1),
        # Try to create as an admin with a correct specified fields
        # The SCTR will be created
        ("admin", "sctr_dict", 201, 2),
        # Try to create as a pm with no specified fields
        # The SCTR won't be created
        ("pm", None, 400, 1),
        # Try to create as a pm with a correct specified fields
        # The SCTR will be created
        ("pm", "sctr_dict", 201, 2),
    ]
)
def test_sctr_create(
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

    if count == 2:
        current_sctr = SCTR.objects.filter(
            unique_identifier=sctr_info["unique_identifier"]
        ).first()

        assert current_sctr.company == user.company


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, data, status_code", [
        # Try to update as unauthorized user
        # The user is not allowed to update it
        (None, dict(), 401),
        (None, {"marketing_name": "aaaaa"}, 401),
        # Try to update a SCTR as an admin with no specified fields
        # The request will be successful, but without any changes
        ("admin", dict(), 200),
        # Try to update a SCTR as an admin with specified fields
        # Changes will be applied
        ("admin", {"marketing_name": "aaaaa"}, 200),
        # Try to update a SCTR as a PM with no specified fields
        # The request will be successful, but without any changes
        ("pm", dict(), 200),
        # Try to update a SCTR as a PM with specified fields
        # Changes will be applied
        ("pm", {"marketing_name": "aaaaa"}, 200)
    ]
)
def test_sctr_update_same_company(
    request, client, auth_header,
    sctr, user, data, status_code
):
    """Tests SCTR update url with the same user and SCTR company."""
    # credentials must be a dict to pass them to the post request
    credentials = dict()
    # If parameter is not empty, replace it with actual data
    if user:
        # user is a fixture with parameters
        user = request.getfixturevalue(user)
        user = user(company=sctr.company)
        credentials = auth_header(user)

    # Move SCTR to draft, so it is editable
    sctr.state = SCTR_STATES.DRAFT
    sctr.save()

    response = client.patch(
        reverse(
            "sctr-patch",
            kwargs={"unique_identifier": sctr.unique_identifier}
        ),
        data=data,
        content_type="application/json",
        **credentials
    )

    assert response.status_code == status_code
    # Ensure data was changed
    if "marketing_name" in data and user:
        assert SCTR.objects.get(
            unique_identifier=sctr.unique_identifier
        ).marketing_name == data["marketing_name"]


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, data, status_code", [
        # Try to update as unauthorized user
        # The user is not allowed to update it
        (None, dict(), 401),
        (None, {"marketing_name": "aaaaa"}, 401),
        # Try to update a SCTR as an admin with no specified fields
        # The user is not allowed to update it
        ("admin", dict(), 403),
        # Try to update a SCTR as an admin with specified fields
        # The user is not allowed to update it
        ("admin", {"marketing_name": "aaaaa"}, 403),
        # Try to update a SCTR as a PM with no specified fields
        # The user is not allowed to update it
        ("pm", dict(), 403),
        # Try to update a SCTR as a PM with specified fields
        # The user is not allowed to update it
        ("pm", {"marketing_name": "aaaaa"}, 403)
    ]
)
def test_sctr_update_different_company(
    request, client, auth_header,
    sctr, user, data, status_code
):
    """Tests SCTR update url with different user and SCTR companies."""
    # credentials must be a dict to pass them to the post request
    credentials = dict()
    # If parameter is not empty, replace it with actual data
    if user:
        # user is a fixture with parameters
        user = request.getfixturevalue(user)
        user = user()
        credentials = auth_header(user)

    # Move SCTR to draft, so it is editable
    sctr.state = SCTR_STATES.DRAFT
    sctr.save()

    response = client.patch(
        reverse(
            "sctr-patch",
            kwargs={"unique_identifier": sctr.unique_identifier}
        ),
        data=data,
        content_type="application/json",
        **credentials
    )

    assert response.status_code == status_code
    # If data and user were specified
    # Ensure data wasn't changed
    if "marketing_name" in data and user:
        assert SCTR.objects.get(
            unique_identifier=sctr.unique_identifier
        ).marketing_name != data["marketing_name"]
