from django import forms
from .models import Vendor, Product, Statement

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'address', 'contact_number', 'due_amount']

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance', None)
        super(VendorForm, self).__init__(*args, **kwargs)



    def clean_vendor_name(self):
        vendor_name = self.cleaned_data.get('vendor_name')
        # Exclude the current instance from the check
        if self.instance and self.instance.vendor_name == vendor_name:
            return vendor_name  # No change, so it’s fine
        if Vendor.objects.filter(vendor_name=vendor_name).exclude(id=self.instance.id if self.instance else None).exists():
            raise forms.ValidationError("Vendor name already exists.")
        return vendor_name

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        # Exclude the current instance from the check
        if self.instance and self.instance.contact_number == contact_number:
            return contact_number  # No change, so it’s fine
        if contact_number and Vendor.objects.filter(contact_number=contact_number).exclude(id=self.instance.id if self.instance else None).exists():
            raise forms.ValidationError("Contact number already exists.")
        return contact_number

class ProductForm(forms.ModelForm):
    date_of_order = forms.DateField(required=True, label='Date of Order', widget=forms.DateInput(attrs={'type': 'date', 'id': 'id_date_of_order'}))

    class Meta:
        model = Product
        fields = ['product_name', 'description', 'quantity_supplied', 'unit_price','selling_price',  'date_of_order', 'paid_amount']
        widgets = {
            'quantity_supplied': forms.NumberInput(attrs={'min': '0', 'id': 'id_quantity_supplied', 'onkeypress': "return (event.charCode != 8 && event.charCode >= 48 && event.charCode <= 57)"}),
            'unit_price': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'id': 'id_unit_price'}),
            'selling_price': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'id': 'id_selling_price'}),
            'paid_amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'id': 'id_paid_amount'}),
        }

    def save(self, commit=True):
        product = super().save(commit=False)
        product.date_of_order = self.cleaned_data['date_of_order']
        product.total_price = product.quantity_supplied * product.unit_price
        product.due_amount =  product.total_price - product.paid_amount
        if commit:
            product.save()
        return product

class PaymentForm(forms.Form):
    amount = forms.FloatField(
        min_value=0.01,  # Ensures the amount is positive and not zero
        label="Amount",
        widget=forms.NumberInput(attrs={'step': '0.01', 'id': 'amount', 'required': True})
    )

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Payment amount must be greater than zero.")
        return amount

class StatementForm(forms.ModelForm):
    class Meta:
        model = Statement
        fields = ['date', 'debit', 'credit']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }