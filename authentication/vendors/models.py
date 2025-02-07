from django.db import models
from datetime import datetime

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    quantity_supplied = models.FloatField()
    unit_price = models.FloatField()
    total_price = models.FloatField()
    date_of_order = models.DateField()
    paid_amount = models.FloatField(default='')
    due_amount = models.FloatField(default='')

    class Meta:
        abstract = True

class Vendor(models.Model):
    vendor_name = models.CharField(max_length=100, unique= True)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True, unique = True)
    due_amount = models.FloatField(blank=True, null=True, default=0.0)
    products = models.JSONField(default=list, blank=True, null=True)
    is_due = models.BooleanField(default=False)  # Red or Green dot based on this status
    created_at = models.DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return self.vendor_name