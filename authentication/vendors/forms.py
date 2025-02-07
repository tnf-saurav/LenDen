from django import forms
from .models import Vendor, Product

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'address', 'contact_number', 'due_amount', 'advance_paid']

    def clean_vendor_name(self):
        vendor_name = self.cleaned_data.get('vendor_name')
        if Vendor.objects.filter(vendor_name=vendor_name).exists():
            raise forms.ValidationError("Vendor name already exists.")
        return vendor_name

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if contact_number and Vendor.objects.filter(contact_number=contact_number).exists():
            raise forms.ValidationError("Contact number already exists.")
        return contact_number

class ProductForm(forms.ModelForm):
    date_of_order = forms.DateField(required=True, label='Date of Order', widget=forms.DateInput(attrs={'type': 'date', 'id': 'id_date_of_order'}))

    class Meta:
        model = Product
        fields = ['product_name', 'description', 'quantity_supplied', 'unit_price', 'total_price', 'date_of_order']

    def save(self, commit=True):
        product = super().save(commit=False)
        product.date_of_order = self.cleaned_data['date_of_order']
        if commit:
            return product
        return product