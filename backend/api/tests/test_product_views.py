"""Module contains test for the following url names.

product-create, product-get
product-patch-delete-retrieve
"""
import pytest
from api.models import Product
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
        product_info = request.getfixturevalue(product_info)

    response = client.post(
        reverse("product-create"),
        data=product_info,
        **credentials
    )

    assert response.status_code == status_code
    assert len(Product.objects.all()) == count

    if count == 2:
        current_product = Product.objects.filter(
            sku_id=product_info["sku_id"]
        ).first()

        assert current_product.company == user.company


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, data, status_code", [
        # Try to update as unauthorized user
        # The user is not allowed to update it
        (None, dict(), 401),
        (None, {"sctr_cogs": "30"}, 401),
        # Try to update a product as an admin with no specified fields
        # The request will be successful, but without any changes
        ("admin", dict(), 200),
        # Try to update a product as an admin with specified fields
        # Changes will be applied
        ("admin", {"sctr_cogs": "30"}, 200),
        # Try to update a product as a PM with no specified fields
        # The request will be successful, but without any changes
        ("pm", dict(), 200),
        # Try to update a product as a PM with specified fields
        # Changes will be applied
        ("pm", {"sctr_cogs": "30"}, 200)
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

    response = client.patch(
        reverse(
            "product-patch-delete-retrieve",
            kwargs={"sku_id": product.sku_id}
        ),
        data=data,
        content_type="application/json",
        **credentials
    )

    assert response.status_code == status_code
    # If data and user were specified
    if data and user:
        assert Product.objects.get(sku_id=product.sku_id).sctr_cogs == 30


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "user, data, status_code", [
        # Try to update as unauthorized user
        # The user is not allowed to update it
        (None, dict(), 401),
        (None, {"sctr_cogs": "30"}, 401),
        # Try to update a product as an admin with no specified fields
        ("admin", dict(), 403),
        # Try to update a product as an admin with specified fields
        ("admin", {"sctr_cogs": "30"}, 403),
        # Try to update a product as a PM with no specified fields
        ("pm", dict(), 403),
        # Try to update a product as a PM with specified fields
        ("pm", {"sctr_cogs": "30"}, 403)
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

    response = client.patch(
        reverse(
            "product-patch-delete-retrieve",
            kwargs={"sku_id": product.sku_id}
        ),
        data=data,
        content_type="application/json",
        **credentials
    )

    assert response.status_code == status_code
    # If data and user were specified
    if data and user:
        assert Product.objects.get(sku_id=product.sku_id).sctr_cogs != data["sctr_cogs"]
