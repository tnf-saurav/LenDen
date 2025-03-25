from django.shortcuts import render, redirect, get_object_or_404
from .models import Vendor, Product, Statement
from .forms import VendorForm, ProductForm, PaymentForm
import uuid
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
import pdfkit
from datetime import datetime
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
import pandas as pd
import re


@login_required
def vendors_list(request):
    vendors = Vendor.objects.filter(user=request.user)
    add_vendor_form = VendorForm()  # Create an empty form for the Add Vendor modal
    return render(request, 'vendors/vendors_list.html', {
        'vendors': vendors,
        'add_vendor_form': add_vendor_form,
    })


def add_vendor(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.user = request.user
            vendor.due_amount = 0.0  # Explicitly set due_amount for new vendors
            vendor.save()
            messages.success(request, 'Vendor added successfully!')
            return redirect('vendors_list')
        else:
            messages.error(request, 'Failed to add the vendor. Please check the form for errors.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            # Re-render the vendors_list page with the form errors
            vendors = Vendor.objects.filter(user=request.user)
            return render(request, 'vendors/vendors_list.html', {
                'vendors': vendors,
                'add_vendor_form': form,
            })
    # For GET requests, redirect to vendors_list (modal is pre-rendered there)
    return redirect('vendors_list')

@login_required
def edit_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id, user=request.user)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vendor updated successfully!')
            return redirect('vendors_list')
        else:
            messages.error(request, 'Failed to update the vendor')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            # Re-render the vendors_list page with the form errors
            vendors = Vendor.objects.filter(user=request.user)
            add_vendor_form = VendorForm()  # For the Add Vendor modal
            return render(request, 'vendors/vendors_list.html', {
                'vendors': vendors,
                'add_vendor_form': add_vendor_form,
                'edit_vendor_form': form,  # Pass the form with errors for the Edit Vendor modal
                'edit_vendor_id': vendor_id,  # To re-open the modal with JavaScript
            })
    # For GET requests, redirect to vendors_list (modal is pre-rendered there)
    return redirect('vendors_list')


@login_required
def delete_vendor(request, vendor_id):
    if request.method == 'POST' and request.POST.get('_method') == 'DELETE':
        vendor = get_object_or_404(Vendor, id=vendor_id, user=request.user)
        vendor.delete()
        return redirect('vendors_list')
    return redirect('vendors_list')

# @login_required
# def vendors_detail(request, vendor_id):
#     vendor = get_object_or_404(Vendor, id=vendor_id, user=request.user)
#     products = Product.objects.filter(vendor=vendor)
#     # vendor.due_amount = sum(product.due_amount for product in products)
#     # vendor.is_due = vendor.due_amount > 0
#     # vendor.save()
#     statements = Statement.objects.filter(vendor=vendor)
#     add_product_form = ProductForm()  # Create an empty form for the Add Product modal
#     payment_form = PaymentForm()
#     return render(request, 'vendors/vendors_detail.html', {
#         'vendor': vendor,
#         'products': products,
#         'statements': statements,
#         'add_product_form': add_product_form,
#         'payment_form': payment_form,
#     })
@login_required
def vendors_detail(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id, user=request.user)
    
    # Get the product_id from the query parameter (if present)
    product_id = request.GET.get('product_id')
    
    # Filter products based on vendor and optionally product_id
    if product_id:
        products = Product.objects.filter(vendor=vendor, id=product_id)
    else:
        products = Product.objects.filter(vendor=vendor)
    
    # vendor.due_amount = sum(product.due_amount for product in products)
    # vendor.is_due = vendor.due_amount > 0
    # vendor.save()
    statements = Statement.objects.filter(vendor=vendor)
    add_product_form = ProductForm()  # Create an empty form for the Add Product modal
    payment_form = PaymentForm()
    
    return render(request, 'vendors/vendors_detail.html', {
        'vendor': vendor,
        'products': products,
        'statements': statements,
        'add_product_form': add_product_form,
        'payment_form': payment_form,
    })

@login_required
def add_product(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id, user=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = vendor
            product.save()
            vendor.due_amount = sum(p.due_amount for p in Product.objects.filter(vendor=vendor))
            vendor.is_due = vendor.due_amount > 0
            vendor.save()
            messages.success(request, 'Product added successfully!')
            return redirect('vendors_detail', vendor_id=vendor.id)
        else:
            messages.error(request, 'Failed to add the product. Please check the form for errors.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            # Re-render the vendors_detail page with the form errors
            products = Product.objects.filter(vendor=vendor)
            statements = Statement.objects.filter(vendor=vendor)
            return render(request, 'vendors/vendors_detail.html', {
                'vendor': vendor,
                'products': products,
                'statements': statements,
                'add_product_form': form,
            })
    # For GET requests, redirect to vendors_detail (modal is pre-rendered there)
    return redirect('vendors_detail', vendor_id=vendor.id)

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    vendor = product.vendor

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        print(f"Form data: {form.data}")  # Debug: Print the submitted form data
        print(f"Product before save: {product.__dict__}")  # Debug: Print the product state before saving
        if form.is_valid():
            updated_product = form.save()
            print(f"Product after save: {updated_product.__dict__}")  # Debug: Print the product state after saving
            vendor.due_amount = sum(p.due_amount for p in Product.objects.filter(vendor=vendor))
            vendor.is_due = vendor.due_amount > 0
            vendor.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('vendors_detail', vendor_id=vendor.id)
        else:
            # Display form errors if validation fails
            messages.error(request, 'Failed to update the product. Please check the form for errors.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            # Re-render the vendors_detail page with the form errors
            products = Product.objects.filter(vendor=vendor)
            statements = Statement.objects.filter(vendor=vendor)
            add_product_form = ProductForm()  # For the Add Product modal
            return render(request, 'vendors/vendors_detail.html', {
                'vendor': vendor,
                'products': products,
                'statements': statements,
                'add_product_form': add_product_form,
                'edit_product_form': form,  # Pass the form with errors for the Edit Product modal
                'edit_product_id': product_id,  # To re-open the modal with JavaScript
            })
    # For GET requests, redirect to vendors_detail (modal is pre-rendered there)
    return redirect('vendors_detail', vendor_id=vendor.id)

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


@login_required
def pay_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id, user=request.user)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            
            # Directly subtract the payment from the vendor's due_amount
            # If due_amount > 0 (amount owed), this reduces the debt
            # If due_amount < 0 (advance), this increases the advance (makes it more negative)
            # If due_amount = 0, this results in an advance (negative due_amount)
            vendor.due_amount -= amount
            vendor.is_due = vendor.due_amount > 0
            vendor.save()

            # Create a statement entry for the payment
            Statement.objects.create(
                vendor=vendor,
                date=datetime.now().date(),
                debit=amount,  # Use debit to indicate money paid out
                total=vendor.due_amount  # Record the new balance
            )

            messages.success(request, f"Payment of Rs. {amount:.2f} recorded successfully!")
            return redirect('vendors_detail', vendor_id=vendor.id)
        else:
            messages.error(request, 'Failed to process the payment. Please check the form for errors.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            # Re-render the vendors_detail page with the form errors
            products = Product.objects.filter(vendor=vendor)
            statements = Statement.objects.filter(vendor=vendor)
            add_product_form = ProductForm()
            return render(request, 'vendors/vendors_detail.html', {
                'vendor': vendor,
                'products': products,
                'statements': statements,
                'add_product_form': add_product_form,
                'payment_form': form,
            })
    # For GET requests, redirect to vendors_detail
    return redirect('vendors_detail', vendor_id=vendor.id)

def generate_statement_data(vendor):
    # Step 1: Get product transactions (incoming: total worth of products)
    products = Product.objects.filter(vendor=vendor).order_by('date_of_order')
    product_transactions = []
    for product in products:
        product_transactions.append({
            'date': product.date_of_order,
            'description': product.product_name,
            'incoming': product.total_price,
            'paid': product.paid_amount,
        })

    # Step 2: Get payment transactions (outgoing: payments made to vendor via pay_vendor)
    statements = Statement.objects.filter(vendor=vendor).order_by('date')
    payment_transactions = []
    for statement in statements:
        if statement.debit > 0:
            payment_transactions.append({
                'date': statement.date,
                'description': "Payment to Vendor",
                'incoming': 0.0,
                'paid': statement.debit,
            })

    # Step 3: Combine all transactions into a single list
    all_transactions = product_transactions + payment_transactions

    # Step 4: Sort transactions by date
    all_transactions.sort(key=lambda x: x['date'])

    # Step 5: Create a Pandas DataFrame
    ledger_df = pd.DataFrame(all_transactions)

    # Step 6: Calculate the running balance and split into Debit and Credit
    if not ledger_df.empty:
        ledger_df['balance'] = ledger_df['incoming'].cumsum() - ledger_df['paid'].cumsum()
        ledger_df['debit'] = ledger_df['balance'].apply(lambda x: x if x > 0 else 0.0)
        ledger_df['credit'] = ledger_df['balance'].apply(lambda x: abs(x) if x < 0 else 0.0)
    else:
        ledger_df['balance'] = 0.0
        ledger_df['debit'] = 0.0
        ledger_df['credit'] = 0.0

    # Step 7: Prepare the statement for the template
    statement = {
        'transactions': ledger_df.to_dict(orient='records'),
        'total_incoming': ledger_df['incoming'].sum() if not ledger_df.empty else 0.0,
        'total_paid': ledger_df['paid'].sum() if not ledger_df.empty else 0.0,
        'final_debit': ledger_df['debit'].iloc[-1] if not ledger_df.empty else 0.0,
        'final_credit': ledger_df['credit'].iloc[-1] if not ledger_df.empty else 0.0,
    }
    return statement

@login_required
def vendor_statement_view(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id, user=request.user)
    statement = generate_statement_data(vendor)
    return render(request, 'vendors/vendor_statement.html', {
        'vendor': vendor,
        'statement': statement,
    })

@login_required
def vendor_statement_pdf(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id, user=request.user)
    statement = generate_statement_data(vendor)

    # Render the PDF template
    template_path = 'vendors/statement_pdf.html'
    context = {
        'vendor': vendor,
        'statement': statement,
    }
    html = render_to_string(template_path, context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')

    # Generate the filename: vendor_name_date_time.pdf
    # Sanitize the vendor name (replace spaces and special characters with underscores)
    vendor_name = re.sub(r'[^a-zA-Z0-9]', '_', vendor.vendor_name.strip())
    # Get the current date and time
    current_time = datetime.now()
    date_str = current_time.strftime('%Y-%m-%d')
    time_str = current_time.strftime('%H%M%S')
    # Construct the filename
    filename = f"{vendor_name}_{date_str}_{time_str}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Generate PDF using xhtml2pdf
    pisa_status = pisa.CreatePDF(
        html.encode('utf-8'),
        dest=response,
        encoding='utf-8'
    )

    if pisa_status.err:
        return HttpResponse('We had some errors with PDF generation <pre>' + html + '</pre>')
    return response