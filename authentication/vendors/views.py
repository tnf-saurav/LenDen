from django.shortcuts import render, redirect, get_object_or_404
from .models import Vendor, Product
from .forms import VendorForm, ProductForm

def vendors_list(request):
    query = request.GET.get('search', '')
    if query:
        vendors = Vendor.objects.filter(vendor_name__icontains(query))
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

def vendors_detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    products = vendor.products
    return render(request, 'vendors/vendors_detail.html', {'vendor': vendor, 'products': products})

def add_product(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    if vendor.products is None:
        vendor.products = []  # Initialize as an empty list if None
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product_dict = {
                'product_name': product.product_name,
                'description': product.description,
                'quantity_supplied': product.quantity_supplied,
                'unit_price': product.unit_price,
                'total_price': product.total_price,
                'date_of_order': str(product.date_of_order),  # Convert date to string
            }
            vendor.products.append(product_dict)
            vendor.save()
            return redirect('vendors_detail', vendor_id=vendor.id)
    else:
        form = ProductForm()
    return render(request, 'vendors/add_product.html', {'form': form, 'vendor': vendor})