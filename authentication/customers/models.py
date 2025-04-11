from django.db import models
from datetime import datetime
from lenden.settings import AUTH_USER_MODEL
import uuid
from authentication.vendors.models import Product

# Get the custom user model
User = AUTH_USER_MODEL

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    due_amount = models.FloatField(blank=True, null=True, default=0.0)
    is_due = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name

class CustomerProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity_bought = models.FloatField()
    unit_price = models.FloatField()
    selling_price = models.FloatField()
    date_of_purchase = models.DateField()
    paid_amount = models.FloatField(default=0.0)

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
    credit = models.FloatField(default=0.0)
    debit = models.FloatField(default=0.0)

    def __str__(self):
        return f"Statement for {self.customer.customer_name} on {self.date}"

    @property
    def total(self):
        debit = self.debit if self.debit is not None else 0.0
        credit = self.credit if self.credit is not None else 0.0
        return debit - credit

class Invoice(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField(default=0.0)
    discount_percent = models.FloatField(default=0.0)
    discount_amount = models.FloatField(default=0.0)

    def __str__(self):
        return f"Invoice for {self.customer.customer_name} - {self.invoice_date}"

    @property
    def final_amount(self):
        return self.total_amount - self.discount_amount

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('vendors.Product', on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit_price = models.FloatField()

    @property
    def total_price(self):
        return self.quantity * self.unit_price

class InvoiceService(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    price = models.FloatField()

    def __str__(self):
        return f"Service for {self.invoice} - {self.description}"