from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory
from django.http import JsonResponse
from .models import Customer, CustomerProduct, CustomerStatement, Invoice, InvoiceItem, InvoiceService
from .forms import CustomerForm, InvoiceForm, InvoiceItemForm, InvoiceServiceForm, PaymentForm
from authentication.vendors.models import Product, Vendor
from datetime import datetime
import pandas as pd
import re
from xhtml2pdf import pisa

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

    unpaid_invoices_total = sum(
        invoice.final_amount 
        for invoice in invoices 
        if not hasattr(invoice, 'is_paid') or not invoice.is_paid
    )
    payments_total = sum(
        statement.debit 
        for statement in statements 
        if statement.debit
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
            has_items = any(form.cleaned_data and not form.cleaned_data.get('DELETE', False) for form in item_formset)
            has_services = any(form.cleaned_data and not form.cleaned_data.get('DELETE', False) for form in service_formset)

            if not has_items and not has_services:
                messages.error(request, "You must add at least one product or one service to the invoice.")
                return render(request, 'customers/invoice.html', {
                    'customer': customer,
                    'invoice_form': invoice_form,
                    'item_formset': item_formset,
                    'service_formset': service_formset,
                    'has_vendor': has_vendor,
                })

            invoice = invoice_form.save(commit=False)
            invoice.customer = customer
            invoice.user = request.user
            invoice.save()

            total = 0.0
            for form in item_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    item = form.save(commit=False)
                    item.invoice = invoice
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
                    total += item.total_price
                    product = item.product
                    product.quantity_supplied -= int(item.quantity)
                    if product.quantity_supplied < 0:
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
                    total += service.price

            invoice.total_amount = total
            discount_percent = invoice.discount_percent
            invoice.discount_amount = total * (discount_percent / 100.0) if discount_percent > 0 else 0.0
            invoice.save()

            # Create a CustomerStatement entry for the invoice
            CustomerStatement.objects.create(
                customer=customer,
                date=invoice.invoice_date.date(),
                credit=invoice.final_amount,  # Invoice increases customer's debt
                debit=0.0,
            )

            customer.due_amount = (customer.due_amount or 0.0) + invoice.final_amount
            customer.save()

            messages.success(request, "Invoice created successfully!")
            return redirect('customers_detail', customer_id=customer.id)
        else:
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
            has_items = any(form.cleaned_data and not form.cleaned_data.get('DELETE', False) for form in item_formset)
            has_services = any(form.cleaned_data and not form.cleaned_data.get('DELETE', False) for form in service_formset)
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

            old_items = {item.id: item for item in InvoiceItem.objects.filter(invoice=invoice)}
            previous_final_amount = invoice.final_amount

            invoice = invoice_form.save(commit=False)
            invoice.customer = customer
            invoice.user = request.user

            total = 0.0
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
                    item.save()
                    total += item.total_price
                    product = item.product
                    if item.id in old_items:
                        old_quantity = old_items[item.id].quantity
                        quantity_diff = old_quantity - item.quantity
                        product.quantity_supplied += int(quantity_diff)
                        del old_items[item.id]
                    else:
                        product.quantity_supplied -= int(item.quantity)
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
                    product = form.instance.product
                    product.quantity_supplied += int(form.instance.quantity)
                    form.instance.delete()
                    if form.instance.id in old_items:
                        del old_items[form.instance.id]
                    product.save()

            for old_item in old_items.values():
                product = old_item.product
                product.quantity_supplied += int(old_item.quantity)
                product.save()

            for form in service_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    service = form.save(commit=False)
                    service.invoice = invoice
                    service.save()
                    total += service.price
                elif form.cleaned_data.get('DELETE', False) and form.instance.pk:
                    form.instance.delete()

            invoice.total_amount = total
            discount_percent = invoice.discount_percent
            invoice.discount_amount = total * (discount_percent / 100.0) if discount_percent > 0 else 0.0
            invoice.save()

            # Update or create CustomerStatement entry for the invoice
            statement, created = CustomerStatement.objects.get_or_create(
                customer=customer,
                date=invoice.invoice_date.date(),
                defaults={'credit': invoice.final_amount, 'debit': 0.0}
            )
            if not created:
                # If statement exists, update the credit (adjust for the difference)
                statement.credit = invoice.final_amount
                statement.debit = 0.0
                statement.save()

            customer.due_amount = (customer.due_amount or 0.0) - previous_final_amount + invoice.final_amount
            customer.save()

            messages.success(request, "Invoice updated successfully!")
            return redirect('customers_detail', customer_id=customer.id)
        else:
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
        vendors = Vendor.objects.filter(user=request.user)
        if not vendors.exists():
            products = Product.objects.none()
        else:
            products = Product.objects.filter(
                vendor__in=vendors,
                product_name__icontains=term,
                inventoryitem__remaining_quantity__gt=0
            ).distinct()[:10]
        results = [{'id': str(p.id), 'label': p.product_name, 'value': p.product_name} for p in products]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)

@login_required
def pay_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, user=request.user)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']  # float
            customer.due_amount = (customer.due_amount or 0.0) - amount
            customer.is_due = customer.due_amount > 0
            customer.save()

            CustomerStatement.objects.create(
                customer=customer,
                date=datetime.now().date(),
                debit=amount,
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

@login_required
def customer_statement(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, user=request.user)

    # Step 1: Get invoice transactions (outgoing: money owed by customer)
    invoices = Invoice.objects.filter(customer=customer).order_by('invoice_date')
    invoice_transactions = []
    for invoice in invoices:
        invoice_transactions.append({
            'date': invoice.invoice_date.date(),
            'description': f"Invoice {request.user.username[:3].upper()}-{customer.id}-{invoice.id}-{invoice.invoice_date.strftime('%Y%m%d')}",
            'outgoing': invoice.final_amount,
            'incoming': 0.0,
        })

    # Step 2: Get payment transactions (incoming: payments made by customer)
    statements = CustomerStatement.objects.filter(customer=customer).order_by('date')
    payment_transactions = []
    for statement in statements:
        if statement.debit > 0:  # Only include payment entries (debit > 0)
            payment_transactions.append({
                'date': statement.date,
                'description': "Payment",
                'outgoing': 0.0,
                'incoming': statement.debit,
            })

    # Step 3: Combine all transactions into a single list
    all_transactions = invoice_transactions + payment_transactions

    # Step 4: Sort transactions by date
    all_transactions.sort(key=lambda x: x['date'])

    # Step 5: Create a Pandas DataFrame
    ledger_df = pd.DataFrame(all_transactions)

    # Step 6: Calculate the running balance and split into Debit and Credit
    if not ledger_df.empty:
        ledger_df['balance'] = ledger_df['outgoing'].cumsum() - ledger_df['incoming'].cumsum()
        # For customers: Positive balance → Debit (customer owes you), Negative balance → Credit (you owe customer)
        ledger_df['debit'] = ledger_df['balance'].apply(lambda x: x if x > 0 else 0.0)
        ledger_df['credit'] = ledger_df['balance'].apply(lambda x: abs(x) if x < 0 else 0.0)
    else:
        ledger_df['balance'] = 0.0
        ledger_df['debit'] = 0.0
        ledger_df['credit'] = 0.0

    # Step 7: Prepare the statement for the template
    statement = {
        'transactions': ledger_df.to_dict(orient='records'),
        'total_outgoing': ledger_df['outgoing'].sum() if not ledger_df.empty else 0.0,
        'total_incoming': ledger_df['incoming'].sum() if not ledger_df.empty else 0.0,
        'final_debit': ledger_df['debit'].iloc[-1] if not ledger_df.empty else 0.0,
        'final_credit': ledger_df['credit'].iloc[-1] if not ledger_df.empty else 0.0,
    }

    return render(request, 'customers/customer_statement.html', {
        'customer': customer,
        'statement': statement,
    })

# @login_required
# def customer_statement_pdf(request, customer_id):
#     customer = get_object_or_404(Customer, id=customer_id, user=request.user)
#     statement = customer_statement(customer)

#     # Render the PDF template
#     template_path = 'customers/statement_pdf.html'
#     context = {
#         'customer': customer,
#         'statement': statement,
#     }
#     html = render_to_string(template_path, context)

#     # Create a PDF response
#     response = HttpResponse(content_type='application/pdf')

#     # Generate the filename: customer_name_date_time.pdf
#     customer_name = re.sub(r'[^a-zA-Z0-9]', '_', customer.customer_name.strip())
#     current_time = datetime.now()
#     date_str = current_time.strftime('%Y-%m-%d')
#     time_str = current_time.strftime('%H%M%S')
#     filename = f"{customer_name}_{date_str}_{time_str}.pdf"
#     response['Content-Disposition'] = f'attachment; filename="{filename}"'

#     # Generate PDF using xhtml2pdf
#     pisa_status = pisa.CreatePDF(
#         html.encode('utf-8'),
#         dest=response,
#         encoding='utf-8'
#     )

#     if pisa_status.err:
#         return HttpResponse('We had some errors with PDF generation <pre>' + html + '</pre>')
#     return response
