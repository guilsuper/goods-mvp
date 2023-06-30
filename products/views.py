from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from store.models import Organization, Member, Product

@login_required(login_url='login')
def dashboard(request):
    total_organization = Organization.objects.count()
    total_member = Member.objects.count()
    total_product = Product.objects.count()
    products = Product.objects.all().order_by('-id')
    context = {
        'organization': total_organization,
        'member': total_member,
        'product': total_product,
        'products': products
    }
    return render(request, 'dashboard.html', context)