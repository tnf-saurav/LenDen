# authentication/dashboard/views.py
# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.db.models import Sum, F, ExpressionWrapper, FloatField
# from datetime import datetime, timedelta
# from authentication.customers.models import Invoice, InvoiceItem, Customer, CustomerStatement  # Adjusted import
# from authentication.vendors.models import Vendor, Statement  # Adjusted import
# from authentication.inventory.models import InventoryItem  # Adjusted import
# from django.utils import timezone

# @login_required
# def dashboard(request):
#     # Get current month and year
#     today = datetime.today()
#     current_month = today.month
#     current_year = today.year

#     # Monthly Sales (using Invoice total_amount)
#     monthly_invoices = Invoice.objects.filter(
#         invoice_date__year=current_year,
#         invoice_date__month=current_month
#     )
#     monthly_sales = monthly_invoices.aggregate(total=Sum('total_amount'))['total'] or 0

#     # Total Customers
#     total_customers = Customer.objects.count()

#     # Total Vendors
#     total_vendors = Vendor.objects.count()

#     # Total Revenue This Year (sum of all invoices for 2025)
#     yearly_invoices = Invoice.objects.filter(invoice_date__year=current_year)
#     total_revenue_year = yearly_invoices.aggregate(total=Sum('total_amount'))['total'] or 0

#     # To Receive (sum of outstanding customer payments)
#     # Assuming 'outstanding_amount' is a field in Customer model; adjust as needed
#     to_receive = Customer.objects.aggregate(total=Sum('outstanding_amount'))['total'] or 0

#     # To Pay (sum of outstanding vendor payments)
#     # Assuming 'due_amount' is a field in Vendor model; adjust as needed
#     to_pay = Vendor.objects.aggregate(total=Sum('due_amount'))['total'] or 0

#     # Sales Trend (daily invoice totals for the current month)
#     sales_trend = []
#     for day in range(1, today.day + 1):
#         daily_sales = Invoice.objects.filter(
#             invoice_date__year=current_year,
#             invoice_date__month=current_month,
#             invoice_date__day=day
#         ).aggregate(total=Sum('total_amount'))['total'] or 0
#         sales_trend.append(daily_sales)

#     # Monthly Sales Trend (monthly invoice totals for the current year)
#     monthly_sales_trend = []
#     for month in range(1, 13):
#         monthly_sales = Invoice.objects.filter(
#             invoice_date__year=current_year,
#             invoice_date__month=month
#         ).aggregate(total=Sum('total_amount'))['total'] or 0
#         monthly_sales_trend.append(monthly_sales)

#     # Sales by Product (using InvoiceItem, ensure 5 items)
#     invoice_ids = monthly_invoices.values_list('id', flat=True)
#     invoice_items = InvoiceItem.objects.filter(invoice_id__in=invoice_ids).select_related('product')
#     product_sales = {}
#     for item in invoice_items:
#         product_name = item.product.product_name
#         total_price = item.quantity * item.unit_price
#         if product_name in product_sales:
#             product_sales[product_name] += total_price
#         else:
#             product_sales[product_name] = total_price
#     sales_by_product = [
#         {'product__product_name': product_name, 'total': total}
#         for product_name, total in sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5]
#     ]

#     # Inventory Status (top 5 products by remaining_quantity)
#     inventory_status = InventoryItem.objects.all().order_by('-remaining_quantity')[:5]

#     context = {
#         'monthly_sales': monthly_sales,
#         'total_customers': total_customers,
#         'total_vendors': total_vendors,
#         'total_revenue_year': total_revenue_year,
#         'to_receive': to_receive,
#         'to_pay': to_pay,
#         'sales_trend': sales_trend,
#         'monthly_sales_trend': monthly_sales_trend,
#         'sales_by_product': sales_by_product,
#         'inventory_status': inventory_status,
#     }
#     return render(request, 'dashboard/dashboard.html', context)

# @login_required
# def dashboard(request):
#     # Get current month and year
#     today = datetime.today()
#     current_month = today.month
#     current_year = today.year

#     # Monthly Sales (using Invoice total_amount)
#     monthly_invoices = Invoice.objects.filter(
#         invoice_date__year=current_year,
#         invoice_date__month=current_month
#     )
#     monthly_sales = monthly_invoices.aggregate(total=Sum('total_amount'))['total'] or 0

#     # Total Customers
#     total_customers = Customer.objects.count()

#     # Total Vendors
#     total_vendors = Vendor.objects.count()

#     # Sales Trend (daily invoice totals for the current month)
#     sales_trend = []
#     for day in range(1, today.day + 1):
#         daily_sales = Invoice.objects.filter(
#             invoice_date__year=current_year,
#             invoice_date__month=current_month,
#             invoice_date__day=day
#         ).aggregate(total=Sum('total_amount'))['total'] or 0
#         sales_trend.append(daily_sales)

#     # Sales by Product (using InvoiceItem)
#     # Step 1: Get invoice IDs for the current month
#     invoice_ids = monthly_invoices.values_list('id', flat=True)

#     # Step 2: Fetch InvoiceItems and calculate total_price in Python
#     invoice_items = InvoiceItem.objects.filter(invoice_id__in=invoice_ids).select_related('product')

#     # Step 3: Aggregate in Python
#     product_sales = {}
#     for item in invoice_items:
#         product_name = item.product.product_name
#         total_price = item.quantity * item.unit_price  # Calculate total_price in Python
#         if product_name in product_sales:
#             product_sales[product_name] += total_price
#         else:
#             product_sales[product_name] = total_price

#     # Step 4: Sort and limit to top 5
#     sales_by_product = [
#         {'product__product_name': product_name, 'total': total}
#         for product_name, total in sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5]
#     ]

#     # Inventory Status (top 5 products by remaining_quantity)
#     inventory_status = InventoryItem.objects.all().order_by('-remaining_quantity')[:5]

#     # Vendor Payments (recent 5 debit transactions from Statement)
#     vendor_payments = Statement.objects.filter(
#         debit__gt=0
#     ).order_by('-date')[:5]

#     context = {
#         'monthly_sales': monthly_sales,
#         'total_customers': total_customers,
#         'total_vendors': total_vendors,
#         'sales_trend': sales_trend,
#         'sales_by_product': sales_by_product,
#         'inventory_status': inventory_status,
#         'vendor_payments': vendor_payments,
#     }
#     return render(request, 'dashboard/dashboard.html', context)


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Count
from django.utils import timezone
from authentication.customers.models import Invoice, InvoiceItem, Customer
from authentication.vendors.models import Vendor
from authentication.inventory.models import InventoryItem, Product

@login_required
def dashboard(request):
    # Get current month and year (timezone-aware)
    today = timezone.now()
    current_month = today.month
    current_year = today.year

    # Monthly Sales (using Invoice total_amount, filtered by user)
    monthly_invoices = Invoice.objects.filter(
        invoice_date__year=current_year,
        invoice_date__month=current_month,
        customer__user__id=request.user.id
    )
    monthly_sales = monthly_invoices.aggregate(total=Sum('total_amount'))['total'] or 0
    print(f"Initial Monthly Sales: {monthly_sales}")


    # Total Customers (filtered by user)
    total_customers = Customer.objects.filter(user__id=request.user.id).count()

    # Total Vendors (filtered by user)
    total_vendors = Vendor.objects.filter(user__id=request.user.id).count()


    # Total Products (filtered by user)
    total_products = Product.objects.filter(vendor__user__id=request.user.id).count()

    # Total Inventory Value (remaining_quantity * unit_price, filtered by user)
    inventory_items = InventoryItem.objects.filter(
        product__vendor__user__id=request.user.id
    ).select_related('product')
    inventory_value = sum(
        item.remaining_quantity * item.product.unit_price
        for item in inventory_items
    ) if inventory_items else 0

    # Total Revenue (Year-to-Date, filtered by user)
    total_revenue = Invoice.objects.filter(
        invoice_date__year=current_year,
        customer__user__id=request.user.id
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    # Sales Trend (daily invoice totals for the current month, filtered by user)
    sales_trend = []
    for day in range(1, today.day + 1):
        daily_sales = Invoice.objects.filter(
            invoice_date__year=current_year,
            invoice_date__month=current_month,
            invoice_date__day=day,
            customer__user__id=request.user.id
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        sales_trend.append(daily_sales)

    # Monthly Sales Trend (monthly invoice totals for the current year, filtered by user)
    monthly_sales_trend = []
    for month in range(1, 13):
        monthly_sales_for_trend = Invoice.objects.filter(
            invoice_date__year=current_year,
            invoice_date__month=month,
            customer__user__id=request.user.id
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        monthly_sales_trend.append(monthly_sales_for_trend)
        print(f"Month {month} Sales: {monthly_sales_for_trend}")
    print(f"Monthly Sales Trend: {monthly_sales_trend}")

    # Inventory Status (top 5 products by remaining_quantity, filtered by user)
    inventory_status = InventoryItem.objects.filter(
        product__vendor__user__id=request.user.id
    ).order_by('-remaining_quantity')[:5]

    # Sales by Product (using InvoiceItem, filtered by user)
    invoice_ids = monthly_invoices.values_list('id', flat=True)
    invoice_items = InvoiceItem.objects.filter(
        invoice_id__in=invoice_ids,
        product__vendor__user__id=request.user.id
    ).select_related('product')

    product_sales = {}
    for item in invoice_items:
        product_name = item.product.product_name
        total_price = item.quantity * item.unit_price
        if product_name in product_sales:
            product_sales[product_name] += total_price
        else:
            product_sales[product_name] = total_price

    sales_by_product = [
        {'product__product_name': product_name, 'total': total}
        for product_name, total in sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5]
    ]
    print(f"Sales by Product: {sales_by_product}")

    context = {
        'monthly_sales': monthly_sales,
        'total_customers': total_customers,
        'total_vendors': total_vendors,
        'total_products': total_products,
        'total_inventory_value': inventory_value,
        'total_revenue': total_revenue,
        'sales_trend': sales_trend,
        'monthly_sales_trend': monthly_sales_trend,
        'sales_by_product': sales_by_product,
        'inventory_status': inventory_status,
        
    }
    print(f"Context Monthly Sales: {context['monthly_sales']}")
    return render(request, 'dashboard/dashboard.html', context)