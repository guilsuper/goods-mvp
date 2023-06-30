from django.urls import path

from .views import (
    create_organization,
    create_member,
    create_product,

    OrganizationListView,
    MemberListView,
    ProductListView,
)

urlpatterns = [
    path('create-organization/', create_organization, name='create-organization'),
    path('create-member/', create_member, name='create-member'),
    path('create-product/', create_product, name='create-product'),

    path('organization-list/', OrganizationListView.as_view(), name='organization-list'),
    path('member-list/', MemberListView.as_view(), name='member-list'),
    path('product-list/', ProductListView.as_view(), name='product-list'),
]