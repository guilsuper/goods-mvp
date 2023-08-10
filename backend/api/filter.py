"""Module with ProductFIlter."""
import django_filters
from api.models import Product


class ProductFilter(django_filters.FilterSet):
    """FIlter for Product objects."""

    class Meta:
        """Metaclas of the ProductFilter."""

        model = Product
        fields = {
            "sku_id": ["icontains"],
            "public_facing_id": ["icontains"],
            "public_facing_name": ["icontains"],
            "description": ["icontains"],

            "sctr_date": ["gt", "lt"],
            "sctr_cogs": ["gte", "lte"],

            "product_input_manufacturer": ["icontains"],
            "product_input_type": ["icontains"],
            "company__company_name": ["exact"]
        }
