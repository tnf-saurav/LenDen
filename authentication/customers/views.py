from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory
from django.http import JsonResponse
from .models import Customer, CustomerProduct, CustomerStatement, Invoice, InvoiceItem, InvoiceService
from .forms import CustomerForm, InvoiceForm, InvoiceItemForm, InvoiceServiceForm, PaymentForm
from authentication.vendors.models import Product, Vendor
from authentication.inventory.models import InventoryItem
from decimal import Decimal
from bson.decimal128 import Decimal128
from datetime import datetime

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

    # Get invoices and statements
    invoices = Invoice.objects.filter(customer=customer)
    statements = CustomerStatement.objects.filter(customer=customer)

    # Calculate due_amount: total unpaid invoices minus payments
    unpaid_invoices_total = sum(
        to_decimal(invoice.final_amount) 
        for invoice in invoices 
        if not hasattr(invoice, 'is_paid') or not invoice.is_paid
    )
    payments_total = sum(
        to_decimal(statement.debit) 
        for statement in statements 
        if statement.debit  # Only count debit entries (payments)
    )
    customer.due_amount = unpaid_invoices_total - payments_total
    customer.is_due = customer.due_amount > 0
    customer.save()

    payment_form = PaymentForm()

    return render(request, 'customers/customers_detail.html', {
        'customer': customer,
        'products': products,
        'statements': statements,
        'invoices': invoices,
        'payment_form': payment_form,
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

@login_required
def edit_invoice(request, customer_id, invoice_id):
    customer = get_object_or_404(Customer, id=customer_id, user=request.user)
    invoice = get_object_or_404(Invoice, id=invoice_id, customer=customer, user=request.user)
    InvoiceItemFormSet = modelformset_factory(InvoiceItem, form=InvoiceItemForm, extra=0, can_delete=True)
    InvoiceServiceFormSet = modelformset_factory(InvoiceService, form=InvoiceServiceForm, extra=0, can_delete=True)

    has_vendor = Vendor.objects.filter(user=request.user).exists()

    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST, instance=invoice)
        item_formset = InvoiceItemFormSet(request.POST, prefix='items', queryset=InvoiceItem.objects.filter(invoice=invoice))
        service_formset = InvoiceServiceFormSet(request.POST, prefix='services', queryset=InvoiceService.objects.filter(invoice=invoice))

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
                messages.error(request, "You must have at least one product or one service in the invoice.")
                return render(request, 'customers/edit_invoice.html', {
                    'customer': customer,
                    'invoice': invoice,
                    'invoice_form': invoice_form,
                    'item_formset': item_formset,
                    'service_formset': service_formset,
                    'has_vendor': has_vendor,
                })

            # Get old items for comparison
            old_items = {item.id: item for item in InvoiceItem.objects.filter(invoice=invoice)}
            previous_final_amount = to_decimal(invoice.final_amount)

            # Save the updated invoice
            invoice = invoice_form.save(commit=False)
            invoice.customer = customer
            invoice.user = request.user

            # Calculate the total from items and services
            total = Decimal('0.0')
            for form in item_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    item = form.save(commit=False)
                    item.invoice = invoice
                    if item.quantity is None or item.unit_price is None:
                        messages.error(request, "Quantity and Unit Price are required for all items.")
                        invoice_form.save()
                        return render(request, 'customers/edit_invoice.html', {
                            'customer': customer,
                            'invoice': invoice,
                            'invoice_form': invoice_form,
                            'item_formset': item_formset,
                            'service_formset': service_formset,
                            'has_vendor': has_vendor,
                        })
                    item.quantity = to_decimal(item.quantity)
                    item.unit_price = to_decimal(item.unit_price)
                    item.save()
                    item_total = to_decimal(item.total_price)
                    total += item_total

                    # Adjust inventory based on difference
                    product = item.product
                    if item.id in old_items:  # Existing item
                        old_quantity = to_decimal(old_items[item.id].quantity)
                        quantity_diff = old_quantity - item.quantity  # Positive means return to inventory, negative means deduct
                        product.quantity_supplied += int(quantity_diff)
                        del old_items[item.id]  # Remove from old_items to track new/deleted items
                    else:  # New item
                        product.quantity_supplied -= int(item.quantity)  # Deduct new quantity

                    if product.quantity_supplied < 0:
                        invoice_form.save()
                        messages.error(request, f"Not enough stock for {product.product_name}. Available: {product.quantity_supplied + int(item.quantity)}.")
                        return render(request, 'customers/edit_invoice.html', {
                            'customer': customer,
                            'invoice': invoice,
                            'invoice_form': invoice_form,
                            'item_formset': item_formset,
                            'service_formset': service_formset,
                            'has_vendor': has_vendor,
                        })
                    product.save()

                elif form.cleaned_data.get('DELETE', False) and form.instance.pk:
                    # Restore stock for deleted items
                    product = form.instance.product
                    product.quantity_supplied += int(to_decimal(form.instance.quantity))
                    form.instance.delete()
                    if form.instance.id in old_items:
                        del old_items[form.instance.id]
                    product.save()

            # Restore stock for any remaining old items (fully removed)
            for old_item in old_items.values():
                product = old_item.product
                product.quantity_supplied += int(to_decimal(old_item.quantity))
                product.save()

            for form in service_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    service = form.save(commit=False)
                    service.invoice = invoice
                    service.price = to_decimal(service.price)
                    service.save()
                    service_price = to_decimal(service.price)
                    total += service_price
                elif form.cleaned_data.get('DELETE', False) and form.instance.pk:
                    form.instance.delete()

            # Update invoice totals and discount
            invoice.total_amount = Decimal(str(total))
            discount_percent = to_decimal(invoice.discount_percent) if invoice.discount_percent is not None else Decimal('0.0')
            if discount_percent > 0:
                invoice.discount_amount = Decimal(str(total * (discount_percent / Decimal('100'))))
            else:
                invoice.discount_amount = Decimal('0.0')
            invoice.save()

            # Update customer due amount
            customer_due = to_decimal(customer.due_amount) if customer.due_amount is not None else Decimal('0.0')
            new_final_amount = to_decimal(invoice.final_amount)
            customer.due_amount = Decimal(str(customer_due - previous_final_amount + new_final_amount))
            customer.save()

            messages.success(request, "Invoice updated successfully!")
            return redirect('customers_detail', customer_id=customer.id)
        else:
            print("Invoice Form Errors:", invoice_form.errors)
            print("Item Formset Errors:", item_formset.errors)
            print("Service Formset Errors:", service_formset.errors)
            messages.error(request, "Error updating invoice. Please check the form.")
    else:
        invoice_form = InvoiceForm(instance=invoice)
        item_formset = InvoiceItemFormSet(queryset=InvoiceItem.objects.filter(invoice=invoice), prefix='items')
        service_formset = InvoiceServiceFormSet(queryset=InvoiceService.objects.filter(invoice=invoice), prefix='services')

    return render(request, 'customers/edit_invoice.html', {
        'customer': customer,
        'invoice': invoice,
        'invoice_form': invoice_form,
        'item_formset': item_formset,
        'service_formset': service_formset,
        'has_vendor': has_vendor,
    })

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

@login_required
def pay_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, user=request.user)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']  # float
            # Convert both to Decimal for arithmetic
            current_due = to_decimal(customer.due_amount)
            payment_amount = Decimal(str(amount))  # Convert float to Decimal
            customer.due_amount = current_due - payment_amount  # Decimal subtraction
            customer.is_due = customer.due_amount > 0
            customer.save()

            # Create statement entry
            CustomerStatement.objects.create(
                customer=customer,
                date=datetime.now().date(),
                debit=amount,  # Store as float or Decimal as per your model
                
            )

            messages.success(request, f"Payment of Rs. {amount:.2f} recorded successfully!")
            return redirect('customers_detail', customer_id=customer.id)
        else:
            messages.error(request, 'Failed to process the payment. Please check the form.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            invoices = Invoice.objects.filter(customer=customer)
            statements = CustomerStatement.objects.filter(customer=customer)
            return render(request, 'customers/customers_detail.html', {
                'customer': customer,
                'invoices': invoices,
                'statements': statements,
                'payment_form': form,
            })
    return redirect('customers_detail', customer_id=customer.id)