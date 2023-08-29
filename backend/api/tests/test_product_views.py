# Copyright 2023 Free World Certified -- all rights reserved.
"""Module contains test for the following url names.

product-create, product-get
product-patch-delete-retrieve
"""
import pytest
from api.models import SCTR
from api.models import SCTR_STATES
from django.urls import reverse


@pytest.mark.django_db()
def test_product_get(client, product):
    """Tests product-get."""
    # Try to get products as unauthorized user
    # Returns all visible products
    response = client.get(reverse("product-get"))

    assert response.status_code == 200
    # If response contains one product information
    assert len(response.json()) == 1


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, product_info, status_code, count", [
        # Try to create as unauthorized user
        # The user is not allowed to create it
        (None, None, 401, 1),
        # Try to create as an admin with no specified fields
        # The product won't be created
        ("admin", None, 400, 1),
        # Try to create as an admin with a correct specified fields
        # The product will be created
        ("admin", "product_dict", 201, 2),
        # Try to create as a pm with no specified fields
        # The product won't be created
        ("pm", None, 400, 1),
        # Try to create as a pm with a correct specified fields
        # The product will be created
        ("pm", "product_dict", 201, 2),
    ]
)
def test_product_create(
    request, client, product,
    auth_header, user, product_info,
    status_code, count
):
    """Tests product-create url."""
    # credentials must be a dict to pass them to the post request
    credentials = dict()
    # If parameter is not empty, replace it with actual data
    if user:
        # user is a fixture with parameters
        user = request.getfixturevalue(user)()
        credentials = auth_header(user)

    # If parameter is not empty, replace it with actual data
    if product_info:
        # If product_info is not None, it contains string "product_dict"
        product_info = request.getfixturevalue(product_info)

    response = client.post(
        reverse("product-create"),
        data=product_info,
        content_type="application/json",
        **credentials
    )

    assert response.status_code == status_code
    assert len(SCTR.objects.all()) == count

    if count == 2:
        current_product = SCTR.objects.filter(
            unique_identifier=product_info["unique_identifier"]
        ).first()

        assert current_product.company == user.company


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, data, status_code", [
        # Try to update as unauthorized user
        # The user is not allowed to update it
        (None, dict(), 401),
        (None, {"marketing_name": "aaaaa"}, 401),
        # Try to update a product as an admin with no specified fields
        # The request will be successful, but without any changes
        ("admin", dict(), 200),
        # Try to update a product as an admin with specified fields
        # Changes will be applied
        ("admin", {"marketing_name": "aaaaa"}, 200),
        # Try to update a product as a PM with no specified fields
        # The request will be successful, but without any changes
        ("pm", dict(), 200),
        # Try to update a product as a PM with specified fields
        # Changes will be applied
        ("pm", {"marketing_name": "aaaaa"}, 200)
    ]
)
def test_product_update_same_company(
    request, client, auth_header,
    product, user, data, status_code
):
    """Tests product update url with the same user and product company."""
    # credentials must be a dict to pass them to the post request
    credentials = dict()
    # If parameter is not empty, replace it with actual data
    if user:
        # user is a fixture with parameters
        user = request.getfixturevalue(user)
        user = user(company=product.company)
        credentials = auth_header(user)

    # Move product to draft, so it is editable
    product.state = SCTR_STATES.draft
    product.save()

    response = client.patch(
        reverse(
            "product-patch",
            kwargs={"unique_identifier": product.unique_identifier}
        ),
        data=data,
        content_type="application/json",
        **credentials
    )

    assert response.status_code == status_code
    # Ensure data was changed
    if "marketing_name" in data and user:
        assert SCTR.objects.get(
            unique_identifier=product.unique_identifier
        ).marketing_name == data["marketing_name"]


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, data, status_code", [
        # Try to update as unauthorized user
        # The user is not allowed to update it
        (None, dict(), 401),
        (None, {"marketing_name": "aaaaa"}, 401),
        # Try to update a product as an admin with no specified fields
        # The user is not allowed to update it
        ("admin", dict(), 403),
        # Try to update a product as an admin with specified fields
        # The user is not allowed to update it
        ("admin", {"marketing_name": "aaaaa"}, 403),
        # Try to update a product as a PM with no specified fields
        # The user is not allowed to update it
        ("pm", dict(), 403),
        # Try to update a product as a PM with specified fields
        # The user is not allowed to update it
        ("pm", {"marketing_name": "aaaaa"}, 403)
    ]
)
def test_product_update_different_company(
    request, client, auth_header,
    product, user, data, status_code
):
    """Tests product update url with different user and product companies."""
    # credentials must be a dict to pass them to the post request
    credentials = dict()
    # If parameter is not empty, replace it with actual data
    if user:
        # user is a fixture with parameters
        user = request.getfixturevalue(user)
        user = user()
        credentials = auth_header(user)

    # Move product to draft, so it is editable
    product.state = SCTR_STATES.draft
    product.save()

    response = client.patch(
        reverse(
            "product-patch",
            kwargs={"unique_identifier": product.unique_identifier}
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
            unique_identifier=product.unique_identifier
        ).marketing_name != data["marketing_name"]
