from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
import uuid

# Get the custom user model
User = get_user_model()

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    due_amount = models.FloatField(blank=True, null=True, default=0.0)
    is_due = models.BooleanField(default=False)  # Red or Green dot based on this status
    created_at = models.DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return self.customer_name

class CustomerProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    quantity_bought = models.FloatField()
    unit_price = models.FloatField()
    selling_price = models.FloatField()
    total_price = models.FloatField()
    date_of_purchase = models.DateField()
    paid_amount = models.FloatField(default=0.0)
    due_amount = models.FloatField(default=0.0)

    def __str__(self):
        return self.product_name

class CustomerStatement(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    credit = models.FloatField(default=0.0)
    debit = models.FloatField(default=0.0)
    total = models.FloatField()

    def __str__(self):
        return f"Statement for {self.customer.customer_name} on {self.date}"