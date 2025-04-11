from django.db import models
from decimal import Decimal
from datetime import datetime
from lenden.settings import AUTH_USER_MODEL
import uuid
from authentication.vendors.models import Product
from bson.decimal128 import Decimal128


# Get the custom user model
User = AUTH_USER_MODEL

def to_decimal(value):
    return Decimal(str(value)) if isinstance(value, Decimal128) else value

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0.0)
    is_due = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name

    # @property
    # def is_due(self):
    #     return self.due_amount > 0

class CustomerProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity_bought = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_purchase = models.DateField()
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return self.product.product_name if self.product else "Deleted Product"

    @property
    def total_price(self):
        return self.quantity_bought * self.selling_price

    @property
    def due_amount(self):
        return self.total_price - self.paid_amount

class CustomerStatement(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Statement for {self.customer.customer_name} on {self.date}"

    @property
    def total(self):
        debit = to_decimal(self.debit) if self.debit is not None else Decimal('0.00')
        credit = to_decimal(self.credit) if self.credit is not None else Decimal('0.00')
        return debit - credit

class Invoice(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Invoice for {self.customer.customer_name} - {self.invoice_date}"

    @property
    def final_amount(self):
        total_amount = Decimal(str(self.total_amount)) if not isinstance(self.total_amount, Decimal) else self.total_amount
        discount_amount = Decimal(str(self.discount_amount)) if not isinstance(self.discount_amount, Decimal) else self.discount_amount
        return total_amount - discount_amount

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('vendors.Product', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        quantity = Decimal(str(self.quantity)) if not isinstance(self.quantity, Decimal) else self.quantity
        unit_price = Decimal(str(self.unit_price)) if not isinstance(self.unit_price, Decimal) else self.unit_price
        return quantity * unit_price

class InvoiceService(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Service for {self.invoice} - {self.description}"