from django.shortcuts import render, get_object_or_404
from .models import InventoryItem

def product_list(request):
    products = InventoryItem.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(InventoryItem, pk=pk)
    return render(request, 'inventory/product_detail.html', {'product': product})