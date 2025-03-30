from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory
from django.http import JsonResponse
from .models import Customer, CustomerProduct, CustomerStatement, Invoice, InvoiceItem, InvoiceService
from .forms import CustomerForm, InvoiceForm, InvoiceItemForm, InvoiceServiceForm
from authentication.vendors.models import Product, Vendor
from authentication.inventory.models import InventoryItem
from decimal import Decimal
from bson.decimal128 import Decimal128

def to_decimal(value):
    return Decimal(str(value)) if isinstance(value, Decimal128) else value

@login_required
def customers_list(request):
    customers = Customer.objects.filter(user=request.user)
    add_customer_form = CustomerForm()
    edit_customer_form = CustomerForm()

    if request.method == 'POST':
        if 'add_customer' in request.POST:
            add_customer_form = CustomerForm(request.POST)
            if add_customer_form.is_valid():
                customer = add_customer_form.save(commit=False)
                customer.user = request.user
                customer.save()
                messages.success(request, f"Customer '{customer.customer_name}' added successfully!")
                return redirect('customers_list')
            else:
                messages.error(request, "Error adding customer. Please check the form.")

        elif 'edit_customer' in request.POST:
            customer_id = request.POST.get('customer_id')
            customer = get_object_or_404(Customer, id=customer_id, user=request.user)
            edit_customer_form = CustomerForm(request.POST, instance=customer)
            if edit_customer_form.is_valid():
                edit_customer_form.save()
                messages.success(request, f"Customer '{customer.customer_name}' updated successfully!")
                return redirect('customers_list')
            else:
                messages.error(request, "Error updating customer. Please check the form.")
                # Pass the customer_id to re-open the modal with errors
                return render(request, 'customers/customers_list.html', {
                    'customers': customers,
                    'add_customer_form': CustomerForm(),
                    'edit_customer_form': edit_customer_form,
                    'edit_customer_id': customer_id,
                })

    return render(request, 'customers/customers_list.html', {
        'customers': customers,
        'add_customer_form': add_customer_form,
        'edit_customer_form': edit_customer_form,
    })


@login_required
def customers_detail(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, user=request.user)
    products = CustomerProduct.objects.filter(customer=customer)
    statements = CustomerStatement.objects.filter(customer=customer)
    invoices = Invoice.objects.filter(customer=customer).prefetch_related('items')

    return render(request, 'customers/customers_detail.html', {
        'customer': customer,
        'products': products,
        'statements': statements,
        'invoices': invoices,
    })


@login_required
def create_invoice(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, user=request.user)
    InvoiceItemFormSet = modelformset_factory(InvoiceItem, form=InvoiceItemForm, extra=1)
    InvoiceServiceFormSet = modelformset_factory(InvoiceService, form=InvoiceServiceForm, extra=1)

    has_vendor = Vendor.objects.filter(user=request.user).exists()

    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST)
        item_formset = InvoiceItemFormSet(request.POST, prefix='items')
        service_formset = InvoiceServiceFormSet(request.POST, prefix='services')

        if invoice_form.is_valid() and item_formset.is_valid() and service_formset.is_valid():
            # Check if there are any items or services
            has_items = False
            has_services = False

            for form in item_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    has_items = True
                    break

            for form in service_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    has_services = True
                    break

            if not has_items and not has_services:
                messages.error(request, "You must add at least one product or one service to the invoice.")
                return render(request, 'customers/invoice.html', {
                    'customer': customer,
                    'invoice_form': invoice_form,
                    'item_formset': item_formset,
                    'service_formset': service_formset,
                    'has_vendor': has_vendor,
                })

            # Save the invoice
            invoice = invoice_form.save(commit=False)
            invoice.customer = customer
            invoice.user = request.user
            invoice.save()

            # Calculate the total from items and services
            total = Decimal('0.0')
            for form in item_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    item = form.save(commit=False)
                    item.invoice = invoice
                    # Ensure quantity and unit_price are set
                    if item.quantity is None or item.unit_price is None:
                        messages.error(request, "Quantity and Unit Price are required for all items.")
                        invoice.delete()
                        return render(request, 'customers/invoice.html', {
                            'customer': customer,
                            'invoice_form': invoice_form,
                            'item_formset': item_formset,
                            'service_formset': service_formset,
                            'has_vendor': has_vendor,
                        })
                    item.save()
                    # Convert total_price to Decimal if it's Decimal128
                    item_total = to_decimal(item.total_price)
                    total += item_total
                    # Deduct the quantity from the product's quantity_supplied
                    product = item.product
                    product.quantity_supplied -= int(item.quantity)  # Convert Decimal to int
                    if product.quantity_supplied < 0:
                        # Roll back the transaction if quantity would go negative
                        invoice.delete()
                        messages.error(request, f"Not enough stock for {product.product_name}. Available: {product.quantity_supplied + int(item.quantity)}.")
                        return render(request, 'customers/invoice.html', {
                            'customer': customer,
                            'invoice_form': invoice_form,
                            'item_formset': item_formset,
                            'service_formset': service_formset,
                            'has_vendor': has_vendor,
                        })
                    product.save()

            for form in service_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    service = form.save(commit=False)
                    service.invoice = invoice
                    service.save()
                    # Convert price to Decimal if it's Decimal128
                    service_price = to_decimal(service.price)
                    total += service_price

            # Update invoice totals and discount
            invoice.total_amount = total
            discount_percent = to_decimal(invoice.discount_percent)
            if discount_percent > 0:
                invoice.discount_amount = total * (discount_percent / Decimal('100'))
            else:
                invoice.discount_amount = Decimal('0.0')
            invoice.save()

            # Update customer due amount
            customer_due = to_decimal(customer.due_amount) if customer.due_amount is not None else Decimal('0.0')
            invoice_final = to_decimal(invoice.final_amount)
            customer.due_amount = customer_due + invoice_final
            customer.save()

            messages.success(request, "Invoice created successfully!")
            return redirect('customers_detail', customer_id=customer.id)
        else:
            print("Invoice Form Errors:", invoice_form.errors)
            print("Item Formset Errors:", item_formset.errors)
            print("Service Formset Errors:", service_formset.errors)
            messages.error(request, "Error creating invoice. Please check the form.")
            return render(request, 'customers/invoice.html', {
                'customer': customer,
                'invoice_form': invoice_form,
                'item_formset': item_formset,
                'service_formset': service_formset,
                'has_vendor': has_vendor,
            })
    else:
        invoice_form = InvoiceForm()
        item_formset = InvoiceItemFormSet(queryset=InvoiceItem.objects.none(), prefix='items')
        service_formset = InvoiceServiceFormSet(queryset=InvoiceService.objects.none(), prefix='services')
        print("Item Formset Forms:", len(item_formset.forms))  # Debug print
        print("Service Formset Forms:", len(service_formset.forms))  # Debug print

    return render(request, 'customers/invoice.html', {
        'customer': customer,
        'invoice_form': invoice_form,
        'item_formset': item_formset,
        'service_formset': service_formset,
        'has_vendor': has_vendor,
    })
# @login_required
# def create_invoice(request, customer_id):
#     customer = get_object_or_404(Customer, id=customer_id)
#     InvoiceItemFormSet = modelformset_factory(InvoiceItem, form=InvoiceItemForm, extra=1)
#     InvoiceServiceFormSet = modelformset_factory(InvoiceService, form=InvoiceServiceForm, extra=1)

#     if request.method == 'POST':
#         invoice_form = InvoiceForm(request.POST)
#         item_formset = InvoiceItemFormSet(request.POST, prefix='items')
#         service_formset = InvoiceServiceFormSet(request.POST, prefix='services')

#         if invoice_form.is_valid() and item_formset.is_valid() and service_formset.is_valid():
#             invoice = invoice_form.save(commit=False)
#             invoice.customer = customer
#             invoice.save()

#             for form in item_formset:
#                 if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
#                     item = form.save(commit=False)
#                     item.invoice = invoice
#                     item.save()

#             for form in service_formset:
#                 if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
#                     service = form.save(commit=False)
#                     service.invoice = invoice
#                     service.save()

#             messages.success(request, "Invoice created successfully!")
#             return redirect('customers_detail', customer_id=customer.id)
#     else:
#         invoice_form = InvoiceForm()
#         item_formset = InvoiceItemFormSet(queryset=InvoiceItem.objects.none(), prefix='items')
#         service_formset = InvoiceServiceFormSet(queryset=InvoiceService.objects.none(), prefix='services')

#     return render(request, 'customers/invoice.html', {
#         'customer': customer,
#         'invoice_form': invoice_form,
#         'item_formset': item_formset,
#         'service_formset': service_formset,
#     })


@login_required
def product_autocomplete(request):
    if 'term' in request.GET:
        term = request.GET['term']
        # Get all vendors associated with the current user
        vendors = Vendor.objects.filter(user=request.user)
        
        if not vendors.exists():
            # If the user has no vendors, return an empty list
            products = Product.objects.none()
        else:
            # Filter products by vendors and product name, and ensure they have stock
            products = Product.objects.filter(
                vendor__in=vendors,  # Products from all vendors of the user
                product_name__icontains=term,
                inventoryitem__remaining_quantity__gt=0  # Only products with stock > 0
            ).distinct()[:10]

        results = [
            {
                'id': str(p.id),
                'label': p.product_name,
                'value': p.product_name,
            } for p in products
        ]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)