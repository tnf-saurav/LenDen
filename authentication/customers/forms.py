from django import forms
from .models import Customer, Invoice, InvoiceItem, InvoiceService, CustomerStatement

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customer_name', 'address', 'contact_number', 'due_amount']
        widgets = {
            'due_amount': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['discount_percent', 'discount_amount']

    def clean(self):
        cleaned_data = super().clean()
        discount_percent = cleaned_data.get('discount_percent')
        discount_amount = cleaned_data.get('discount_amount')
        total_amount = self.instance.total_amount if self.instance else 0.0
        return cleaned_data

class InvoiceItemForm(forms.ModelForm):
    product_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = InvoiceItem
        fields = ['product', 'quantity', 'unit_price']
        widgets = {
            'product': forms.HiddenInput(),
            'quantity': forms.NumberInput(attrs={'min': 1, 'class': 'form-control', 'required': 'required'}),
            'unit_price': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control', 'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.product_id:
                try:
                    product = self.instance.product
                    self.fields['product_name'].initial = product.product_name
                except Product.DoesNotExist:
                    self.fields['product_name'].initial = "Product Deleted"
            else:
                self.fields['product_name'].initial = "Product Missing"

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        product_name = cleaned_data.get('product_name')
        quantity = cleaned_data.get('quantity')
        unit_price = cleaned_data.get('unit_price')

        if product_name and not product:
            raise forms.ValidationError("Please select a valid product from the suggestions.")
        if quantity is None or quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than 0.")
        if unit_price is None or unit_price <= 0:
            raise forms.ValidationError("Unit price must be greater than 0.")
        return cleaned_data

class InvoiceServiceForm(forms.ModelForm):
    class Meta:
        model = InvoiceService
        fields = ['description', 'price']

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price

class PaymentForm(forms.Form):
    amount = forms.FloatField(
        min_value=0.01,
        label="Amount",
        widget=forms.NumberInput(attrs={'step': '0.01', 'id': 'amount', 'required': True})
    )

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Payment amount must be greater than zero.")
        return amount
