from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer, CustomerProduct, CustomerStatement
from .forms import CustomerForm

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

    return render(request, 'customers/customers_detail.html', {
        'customer': customer,
        'products': products,
        'statements': statements,
    })