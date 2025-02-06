from django.shortcuts import render, redirect
from django.http import Http404
from mongoengine import connect
from .models import Vendor, Product
from .forms import VendorForm, ProductForm

# Ensure the MongoDB connection is established
connect('LenDen', host='mongodb://localhost:27017/')

def vendors_list(request):
    query = request.GET.get('search', '')
    if query:
        vendors = Vendor.objects.filter(vendor_name__icontains=query)
    else:
        vendors = Vendor.objects.all()
    
    return render(request, 'vendors/vendors_list.html', {'vendors': vendors})

def add_vendor(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vendors_list')
    else:
        form = VendorForm()
    return render(request, 'vendors/add_vendor.html', {'form': form})

def vendor_detail(request, vendor_id):
    try:
        vendor = Vendor.objects.get(id=vendor_id)
    except Vendor.DoesNotExist:
        raise Http404("Vendor does not exist")
    
    products = vendor.products
    return render(request, 'vendors/vendors_detail.html', {'vendor': vendor, 'products': products})

def add_product(request, vendor_id):
    try:
        vendor = Vendor.objects.get(id=vendor_id)
    except Vendor.DoesNotExist:
        raise Http404("Vendor does not exist")
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            vendor.products.append(product)
            vendor.save()
            return redirect('vendors_detail', vendor_id=vendor.id)
    else:
        form = ProductForm()
    
    return render(request, 'vendors/add_product.html', {'form': form, 'vendor': vendor})