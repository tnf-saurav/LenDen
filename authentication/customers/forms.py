from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customer_name', 'address', 'contact_number', 'due_amount']
        widgets = {
            'due_amount': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }