from django.shortcuts import render, redirect, get_object_or_404
from .models import Vendor, Product, Statement
from .forms import VendorForm, ProductForm
import uuid
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
import pdfkit
from datetime import datetime
from xhtml2pdf import pisa

def vendors_list(request):
    query = request.GET.get('search', '')
    if query:
        vendors = Vendor.objects.filter(vendor_name__icontains(query))
    else:
        vendors = Vendor.objects.all()
    
    # # Update `due_amount` for each vendor before rendering the list
    # for vendor in vendors:
    #     products = vendor.products
    #     due_amount = sum(product['due_amount'] for product in products if 'due_amount' in product)
    #     vendor.due_amount = due_amount
    #     vendor.save()
    
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

def edit_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('vendors_list')
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'vendors/edit_vendor.html', {'form': form, 'vendor': vendor})

def delete_vendor(request, vendor_id):
    if request.method == 'POST' and request.POST.get('_method') == 'DELETE':
        vendor = get_object_or_404(Vendor, id=vendor_id)
        vendor.delete()
        # return JsonResponse({'status': 'success'})
        return redirect('vendors_list')
    # return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    return redirect('vendors_list')

# def vendors_detail(request, vendor_id):
#     vendor = get_object_or_404(Vendor, id=vendor_id)
#     products = vendor.products
    
#     # Ensure that each product dictionary contains the 'due_amount' key
#     for product in products:
#         if 'due_amount' not in product:
#             product['due_amount'] =  product['total_price'] - product['paid_amount']
#     # Calculate due amount for the vendor
#     due_amount = sum(product['due_amount'] for product in products)
#     vendor.due_amount = due_amount
#     vendor.save()
#     statements = Statement.objects.filter(vendor=vendor)
#     return render(request, 'vendors/vendors_detail.html', {'vendor': vendor, 'products': products, 'statements': statements})

def vendors_detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    products = Product.objects.filter(vendor=vendor)
    vendor.due_amount = sum(product.due_amount for product in products)
    vendor.is_due = vendor.due_amount > 0
    vendor.save()
    statements = Statement.objects.filter(vendor=vendor)
    return render(request, 'vendors/vendors_detail.html', {'vendor': vendor, 'products': products, 'statements': statements})


# def add_product(request, vendor_id):
#     vendor = get_object_or_404(Vendor, id=vendor_id)
#     if vendor.products is None:
#         vendor.products = []
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             product = form.save(commit=False)

#             db_product = Product.objects.create(
#                 vendor=vendor,
#                 product_name=product.product_name,
#                 description=product.description,
#                 quantity_supplied=product.quantity_supplied,
#                 unit_price=product.unit_price,
#                 selling_price=product.selling_price,
#                 total_price=product.total_price,
#                 date_of_order=product.date_of_order,
#                 paid_amount=product.paid_amount,
#                 due_amount=product.total_price - product.paid_amount
#             )
            
#             product_dict = {
#                 'id': str(uuid.uuid4()),
#                 'product_name': product.product_name,
#                 'description': product.description,
#                 'quantity_supplied': product.quantity_supplied,
#                 'unit_price': product.unit_price,
#                 'selling_price': product.selling_price,
#                 'total_price': product.total_price,
#                 'date_of_order': str(product.date_of_order),
#                 'paid_amount': product.paid_amount,
#                 'due_amount': product.total_price - product.paid_amount
#             }
#             vendor.products.append(product_dict)
#             vendor.save()
#             return redirect('vendors_detail', vendor_id=vendor.id)
#     else:
#         form = ProductForm()
#     return render(request, 'vendors/add_product.html', {'form': form, 'vendor': vendor})

def add_product(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = vendor
            product.save()
            vendor.due_amount = sum(p.due_amount for p in Product.objects.filter(vendor=vendor))
            vendor.is_due = vendor.due_amount > 0
            vendor.save()
            return redirect('vendors_detail', vendor_id=vendor.id)
    else:
        form = ProductForm()
    return render(request, 'vendors/add_product.html', {'form': form, 'vendor': vendor})


# def edit_product(request, product_id):
#     vendor = get_object_or_404(Vendor, id=request.GET.get('vendor_id'))  
#     product = next((p for p in vendor.products if p['id'] == str(product_id)), None) 
#     if request.method == 'POST':
#         form = ProductForm(request.POST, initial=product)
#         if form.is_valid():
#             updated_product = form.save(commit=False)
#             product.update({
#                 'product_name': updated_product.product_name,
#                 'description': updated_product.description,
#                 'quantity_supplied': updated_product.quantity_supplied,
#                 'unit_price': updated_product.unit_price,
#                 'selling_price': updated_product.selling_price,
#                 'total_price': updated_product.total_price,
#                 'date_of_order': str(updated_product.date_of_order),
#                 'paid_amount': updated_product.paid_amount,
#                 'due_amount': updated_product.total_price - updated_product.paid_amount
#             })
#             vendor.save()
#             return redirect('vendors_detail', vendor_id=vendor.id)
#     else:
#         form = ProductForm(initial=product)
#     return render(request, 'vendors/edit_product.html', {'form': form, 'product': product})
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    vendor = product.vendor
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            vendor.due_amount = sum(p.due_amount for p in Product.objects.filter(vendor=vendor))
            vendor.is_due = vendor.due_amount > 0
            vendor.save()
            return redirect('vendors_detail', vendor_id=vendor.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'vendors/edit_product.html', {'form': form, 'product': product})


def delete_product(request, product_id):
    if request.method == 'DELETE':
        vendor_id = request.GET.get('vendor_id')
        print(f"Vendor ID: {vendor_id}")
        print(f"Product ID: {product_id}")
        vendor = get_object_or_404(Vendor, id=vendor_id)
        print(f"Vendor: {vendor}")
        product = next((p for p in vendor.products if p['id'] == str(product_id)), None)
        print(f"Product: {product}")
        if product:
            vendor.products.remove(product)
            vendor.save()
            print("Product removed successfully")
            return JsonResponse({'status': 'success'})
        else:
            print("Product not found")
            return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
    print("Invalid request method")
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# def pay_vendor(request, vendor_id):
#     vendor = get_object_or_404(Vendor, id=vendor_id)
#     if request.method == 'POST':
#         amount = float(request.POST.get('amount', 0))
#         if amount > 0:
#             vendor.due_amount -= amount
#             vendor.save()
#             Statement.objects.create(vendor=vendor, date=datetime.now().date(), credit=amount, total=vendor.due_amount)
#     return redirect('vendors_detail', vendor_id=vendor.id)

def pay_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    if request.method == 'POST':
        amount = float(request.POST.get('amount', 0))
        if amount > 0:
            products = Product.objects.filter(vendor=vendor)
            total_due = sum(product.due_amount for product in products)
            
            if total_due > 0:
                remaining_payment = amount
                for product in products:
                    if remaining_payment <= 0:
                        break
                    if product.due_amount > 0:
                        payment_for_product = min(remaining_payment, product.due_amount)
                        product.paid_amount += payment_for_product
                        product.due_amount -= payment_for_product
                        remaining_payment -= payment_for_product
                        product.save()
                        # Update corresponding entry in vendor.products
                        for p_dict in vendor.products:
                            if p_dict['product_name'] == product.product_name and p_dict['total_price'] == product.total_price:
                                p_dict['paid_amount'] = product.paid_amount
                                p_dict['due_amount'] = product.due_amount
                                break
            
            vendor.due_amount = sum(product.due_amount for product in Product.objects.filter(vendor=vendor))
            vendor.is_due = vendor.due_amount > 0
            vendor.save()
            
            Statement.objects.create(
                vendor=vendor,
                date=datetime.now().date(),
                credit=amount,
                total=vendor.due_amount
            )
    return redirect('vendors_detail', vendor_id=vendor.id)

def download_statement(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    statements = Statement.objects.filter(vendor=vendor)
    products = vendor.products
    # Create statement entries for each product
    product_statements = [
        {
            'date': product['date_of_order'],
            'credit': product['total_price'],
            'debit': product['paid_amount'],
            'due': product['due_amount']
        } for product in products
    ]
    all_statements = list(statements) + product_statements

    # Calculate total due
    total_due = vendor.due_amount

    html_string = render_to_string('vendors/statement.html', {'vendor': vendor, 'statements': all_statements, 'total_due': total_due})

    # Create a PDF from the HTML string
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{vendor.vendor_name}_{datetime.now().date()}.pdf"'
    pisa_status = pisa.CreatePDF(html_string, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors with code %s' % pisa_status.err, status=500)
    return response