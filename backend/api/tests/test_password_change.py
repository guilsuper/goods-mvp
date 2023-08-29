# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains tests for password changing."""
import pytest
from api.models import Administrator
from django.urls import reverse


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, status_code", [
        ("admin", 200),
    ]
)
def test_product_create(
    request, client,
    auth_header, user,
    status_code
):
    """Tests password changing."""
    # credentials must be a dict to pass them to the post request
    credentials = dict()
    new_password = "12345"
    # If parameter is not empty, replace it with actual data
    if user:
        # user is a fixture with parameters
        user = request.getfixturevalue(user)()
        credentials = auth_header(user)

    response = client.patch(
        reverse("self-patch-delete-retrieve"),
        data={"password": new_password},
        content_type="application/json",
        **credentials
    )

    assert response.status_code == status_code
    # Check that password was hashed
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
