from django.shortcuts import render, redirect, get_object_or_404
from .models import Vendor, Product
from .forms import VendorForm, ProductForm
import uuid

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
            return render(request, 'vendors/add_vendor.html', {'form': form})
    else:
        form = VendorForm()
    return render(request, 'vendors/add_vendor.html', {'form': form})

def vendors_detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    products = vendor.products
    # Ensure that each product dictionary contains the 'due_amount' key
    for product in products:
        if 'due_amount' not in product:
            product['due_amount'] =  product['total_price'] - product['paid_amount']
    # Calculate due amount for the vendor
    due_amount = sum(product['due_amount'] for product in products)
    vendor.due_amount = due_amount
    vendor.save()
    return render(request, 'vendors/vendors_detail.html', {'vendor': vendor, 'products': products})

def add_product(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    if vendor.products is None:
        vendor.products = []
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product_dict = {
                'id': str(uuid.uuid4()),
                'product_name': product.product_name,
                'description': product.description,
                'quantity_supplied': product.quantity_supplied,
                'unit_price': product.unit_price,
                'total_price': product.total_price,
                'date_of_order': str(product.date_of_order),
                'paid_amount': product.paid_amount,
                'due_amount': product.total_price - product.paid_amount
            }
            vendor.products.append(product_dict)
            vendor.save()
            return redirect('vendors_detail', vendor_id=vendor.id)
    else:
        form = ProductForm()
    return render(request, 'vendors/add_product.html', {'form': form, 'vendor': vendor})

def edit_product(request, product_id):
    vendor = get_object_or_404(Vendor, id=request.GET.get('vendor_id'))  
    product = next((p for p in vendor.products if p['id'] == str(product_id)), None) 
    if request.method == 'POST':
        form = ProductForm(request.POST, initial=product)
        if form.is_valid():
            updated_product = form.save(commit=False)
            product.update({
                'product_name': updated_product.product_name,
                'description': updated_product.description,
                'quantity_supplied': updated_product.quantity_supplied,
                'unit_price': updated_product.unit_price,
                'total_price': updated_product.total_price,
                'date_of_order': str(updated_product.date_of_order),
                'paid_amount': updated_product.paid_amount,
                'due_amount': updated_product.total_price - updated_product.paid_amount
            })
            vendor.save()
            return redirect('vendors_detail', vendor_id=vendor.id)
    else:
        form = ProductForm(initial=product)
    return render(request, 'vendors/edit_product.html', {'form': form, 'product': product})

def delete_product(request, product_id):
    vendor_id = request.GET.get('vendor_id')
    vendor = get_object_or_404(Vendor, id=vendor_id)
    product = next((p for p in vendor.products if p['id'] == str(product_id)), None)  
    if request.method == 'POST':
        vendor.products.remove(product)
        vendor.save()
        return redirect('vendors_detail', vendor_id=vendor.id)
    return render(request, 'vendors/delete_product.html', {'product': product})