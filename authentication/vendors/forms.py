# apps/vendors/forms.py

from django import forms
from .models import Vendor
from django.contrib.auth.models import User

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'address', 'contact_number', 'due_amount', 'advance_paid']
        labels = {
            'vendor_name': 'Vendor Name',
            'contact_number': 'Contact Number',
            'due_amount': 'Due Amount',
            'advance_paid': 'Advance Paid'
        }

    class ProductForm(forms.ModelForm):
        class Meta:
            model = Product
            fields = ['product_name', 'description', 'quantity_supplied', 'unit_price', 'total_price', 'date_of_order']
            labels = {
            'product_name': 'Product Name',
            'quantity_supplied': 'Quantity Supplied',
            'unit_price': 'Unit Price',
            'total_price': 'Total Price',
            'date_of_order': 'Date of Order'
        }