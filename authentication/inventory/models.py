from django.db import models
from authentication.vendors.models import Vendor, Product

class InventoryItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    remaining_quantity = models.PositiveIntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product.name