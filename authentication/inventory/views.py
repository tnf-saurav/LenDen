from django.shortcuts import render, get_object_or_404
from .models import InventoryItem
from django.contrib.auth.decorators import login_required

@login_required
def product_list(request):
    products = InventoryItem.objects.filter(product__vendor__user=request.user)
    return render(request, 'inventory/product_list.html', {'products': products})
