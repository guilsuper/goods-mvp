# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains tests for password changing."""
import pytest
from api.models import Administrator
from django.urls import reverse


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, status_code", [
        # Admins can modify their password
        ("admin", 200),
        # PMs have no permission to perform this action
        ("pm", 403),
        # User can't access it
        (None, 401)
    ]
)
def test_password_change(
    request, client,
    auth_header, user,
    status_code
):
    """Tests password changing."""
    # credentials must be a dict to pass them to the post request
    credentials = dict()
    old_password = "12345"
    new_password = old_password + "2"
    # If parameter is not empty, replace it with actual data
    if user:
        # user is a fixture with parameters
        user = request.getfixturevalue(user)(password=old_password)
        credentials = auth_header(user)

    response = client.patch(
        reverse("self-patch-delete-retrieve"),
        data={"password": new_password},
        content_type="application/json",
        **credentials
    )

    assert response.status_code == status_code
    # If changed -- check that password was changed and hashed
    if status_code == 200:
        assert Administrator.objects.get(email=user.email).password != new_password

        # Check if it is possible to login
        response = client.post(
            reverse("token-obtain-pair"),
            data={
                "email": user.email,
                "password": new_password
            }
        )

        assert response.status_code == 200
