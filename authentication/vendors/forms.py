from django import forms
from .models import Vendor, Product

class VendorForm(forms.Form):
    vendor_name = forms.CharField(max_length=100, required=True, label='Vendor Name')
    address = forms.CharField(max_length=255, required=False, label='Address')
    contact_number = forms.CharField(max_length=15, required=False, label='Contact Number')
    due_amount = forms.FloatField(required=False, label='Due Amount')
    advance_paid = forms.FloatField(required=False, label='Advance Paid')

    def save(self, commit=True):
        vendor_data = self.cleaned_data
        vendor = Vendor(**vendor_data)
        if commit:
            vendor.save()
        return vendor

class ProductForm(forms.Form):
    product_name = forms.CharField(max_length=100, required=True, label='Product Name')
    description = forms.CharField(max_length=255, required=False, label='Description')
    quantity_supplied = forms.FloatField(required=True, label='Quantity Supplied')
    unit_price = forms.FloatField(required=True, label='Unit Price')
    total_price = forms.FloatField(required=True, label='Total Price')
    date_of_order = forms.DateTimeField(required=True, label='Date of Order')

    def save(self, commit=True):
        product_data = self.cleaned_data
        product = Product(**product_data)
        if commit:
            product.save()
        return product