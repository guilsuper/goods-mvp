from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from users.models import User
from .models import (
    Organization,
    Member,
    Product
)
from .forms import (
    OrganizationForm,
    MemberForm,
    ProductForm
)

# Organization views
@login_required(login_url='login')
def create_organization(request):
    forms = OrganizationForm()
    if request.method == 'POST':
        forms = OrganizationForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            retype_password = forms.cleaned_data['retype_password']
            if password == retype_password:
                user = User.objects.create_user(username=username, password=password, email=email, is_organization=True)
                Organization.objects.create(user=user, name=name, address=address)
                return redirect('organization-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addOrganization.html', context)


class OrganizationListView(ListView):
    model = Organization
    template_name = 'store/organization_list.html'
    context_object_name = 'organization'


# Member views
@login_required(login_url='login')
def create_member(request):
    forms = MemberForm()
    if request.method == 'POST':
        forms = MemberForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            organization = forms.cleaned_data['organization']
            email = forms.cleaned_data['email']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            retype_password = forms.cleaned_data['retype_password']
            if password == retype_password:
                user = User.objects.create_user(username=username, password=password, email=email, is_member=True)
                Member.objects.create(user=user, name=name, address=address, organization=organization)
                return redirect('member-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addmember.html', context)

class MemberListView(ListView):
    model = Member
    template_name = 'store/member_list.html'
    context_object_name = 'member'

# Product views
@login_required(login_url='login')
def create_product(request):
    forms = ProductForm()
    if request.method == 'POST':
        forms = ProductForm(request.POST)
        if forms.is_valid():
            organization = forms.cleaned_data['organization']
            name = forms.cleaned_data['name']
            description = forms.cleaned_data['description']
            price = forms.cleaned_data['price']
            sku = forms.cleaned_data['sku']
            member = forms.cleaned_data['member']
            Product.objects.create(
                organization=organization,
                name=name,
                description=description,
                price=price,
                sku=sku,
                member=member,
                status='pending'
            )
            return redirect('product-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addProduct.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'
