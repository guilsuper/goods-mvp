"""Module contains test for the following url names.

product-create, product-get
product-patch-delete-retrieve
"""
from api.models import Product
from api.tests.factories.Factories import (
    AdministratorFactory,
    CompanyFactory,
    GroupFactory,
    ProductFactory
)

from django.test import Client, TestCase
from django.urls import reverse

from rest_framework_simplejwt.tokens import AccessToken


class TestProductViews(TestCase):
    """Tests for product views."""

    def setUp(self):
        """Admin, client and product setup."""
        self.client = Client()

        self.admin_group = GroupFactory(name="Administrator")
        self.company = CompanyFactory()

        self.email = "admin@gmail.com"
        self.password = "admin"
        self.admin = AdministratorFactory(
            email=self.email,
            password=self.password,
            company=self.company
        )
        self.admin.groups.add(self.admin_group)

        self.pm_email = "pmpm@gmail.com"
        self.pm_password = "pmpm"
        self.pm = AdministratorFactory(
            email=self.pm_email,
            password=self.pm_password,
            groups=[GroupFactory(name="PM")],
            company=self.company
        )
        self.admin2 = AdministratorFactory()

        self.access_token_admin = str(AccessToken.for_user(self.admin))
        self.credentials_admin = {
            "HTTP_AUTHORIZATION": "Bearer " + self.access_token_admin
        }

        self.access_token_pm = str(AccessToken.for_user(self.pm))
        self.credentials_pm = {
            "HTTP_AUTHORIZATION": "Bearer " + self.access_token_pm
        }

        self.product = ProductFactory(company=self.company)
        self.product2 = ProductFactory(company=self.admin2.company)
        self.product_dict = ProductFactory.build().__dict__
        self.product_dict.pop("id")
        self.product_dict.pop("company_id")

    def test_product_get(self):
        """Tests product-get."""
        # Try to get products as unauthorized user
        # Returns all visible products
        response = self.client.get(reverse("product-get"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), len(Product.objects.all()))

    def test_product_create_no_auth(self):
        """Tests product-create url with no headers."""
        # Try to create as unauthorized user
        # The user is not allowed to create it
        response = self.client.post(reverse("product-create"))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(len(Product.objects.all()), 2)

    def test_product_create_admin(self):
        """Product-create url as administrator."""
        # Try to create as an admin with no specified fields
        # The product won't be created
        response = self.client.post(
            reverse("product-create"),
            **self.credentials_admin
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(Product.objects.all()), 2)

        # Try to create as an admin with a correct specified fields
        # The product will be created
        response = self.client.post(
            reverse("product-create"),
            data=self.product_dict,
            **self.credentials_admin
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Product.objects.all()), 3)

        current_product = Product.objects.filter(
            sku_id=self.product_dict["sku_id"]
        ).first()

        self.assertEqual(current_product.company, self.admin.company)

    def test_product_create_pm(self):
        """Product-create url as PM."""
        # Try to create as a pm with no specified fields
        # The product won't be created
        response = self.client.post(
            reverse("product-create"),
            **self.credentials_pm
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(Product.objects.all()), 2)

        # Try to create as a pm with a correct specified fields
        # The product will be created
        response = self.client.post(
            reverse("product-create"),
            data=self.product_dict,
            **self.credentials_pm
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Product.objects.all()), 3)

        current_product = Product.objects.filter(
            sku_id=self.product_dict["sku_id"]
        ).first()

        self.assertEqual(current_product.company, self.admin.company)

    def test_product_update_no_auth(self):
        """Tests product update url with no headers."""
        # Try to update a product as unauthorized user
        # The user is not allowed to update it
        response = self.client.patch(
            reverse(
                "product-patch-delete-retrieve",
                kwargs={"sku_id": self.product.sku_id}
            ),
            data={"sctr_cogs": 30}
        )

        self.assertEqual(response.status_code, 401)

    def test_product_update_admin(self):
        """Tests product update url as administrator."""
        # Try to update a product as an admin with no specified fields
        # The request will be successful, but without any changes
        response = self.client.patch(
            reverse(
                "product-patch-delete-retrieve",
                kwargs={"sku_id": self.product.sku_id}
            ),
            **self.credentials_admin
        )

        self.assertEqual(response.status_code, 200)

        # Try to update a product as an admin with specified fields
        # Changes will be applied
        response = self.client.patch(
            reverse(
                "product-patch-delete-retrieve",
                kwargs={"sku_id": self.product.sku_id}
            ),
            data={"sctr_cogs": "30"},
            content_type="application/json",
            **self.credentials_admin
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Product.objects.get(sku_id=self.product.sku_id).sctr_cogs,
            30
        )

        # Try to update not the own product as an admin with specified fields
        # The admin is not allowed to update it
        response = self.client.patch(
            reverse(
                "product-patch-delete-retrieve",
                kwargs={"sku_id": self.product2.sku_id}
            ),
            data={"sctr_cogs": "30"},
            content_type="application/json",
            **self.credentials_admin
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            Product.objects.get(sku_id=self.product2.sku_id).sctr_cogs,
            self.product2.sctr_cogs
        )

    def test_product_update_pm(self):
        """Tests product update url as a PM."""
        # Try to update a product as a PM with no specified fields
        # The request will be successful, but without any changes
        response = self.client.patch(
            reverse(
                "product-patch-delete-retrieve",
                kwargs={"sku_id": self.product.sku_id}
            ),
            **self.credentials_pm
        )

        self.assertEqual(response.status_code, 200)

        # Try to update a product as a PM with specified fields
        # Changes will be applied
        response = self.client.patch(
            reverse(
                "product-patch-delete-retrieve",
                kwargs={"sku_id": self.product.sku_id}
            ),
            data={"sctr_cogs": "30"},
            content_type="application/json",
            **self.credentials_pm
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Product.objects.get(sku_id=self.product.sku_id).sctr_cogs,
            30
        )

        # Try to update not the own product as a PM with specified fields
        # The PM is not allowed to update it
        response = self.client.patch(
            reverse(
                "product-patch-delete-retrieve",
                kwargs={"sku_id": self.product2.sku_id}
            ),
            data={"sctr_cogs": "30"},
            content_type="application/json",
            **self.credentials_pm
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            Product.objects.get(sku_id=self.product2.sku_id).sctr_cogs,
            self.product2.sctr_cogs
        )
