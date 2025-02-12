from django.db import models
from datetime import datetime
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

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

class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    quantity_supplied = models.FloatField()
    unit_price = models.FloatField()
    total_price = models.FloatField()
    date_of_order = models.DateField()
    paid_amount = models.FloatField(default='')
    due_amount = models.FloatField(default='')

    # class Meta:
    #     abstract = True
    def __str__(self):
        return self.product_name


@receiver(post_save, sender=Product)
def create_or_update_inventory(sender, instance, created, **kwargs):
    from inventory.models import InventoryItem
    if created:
        InventoryItem.objects.create(product=instance, remaining_quantity=instance.quantity_supplied, selling_price=instance.unit_price)
    else:
        inventory_item = InventoryItem.objects.get(product=instance)
        inventory_item.remaining_quantity = instance.quantity_supplied
        inventory_item.selling_price = instance.unit_price
        inventory_item.save()

@receiver(post_delete, sender=Product)
def delete_inventory(sender, instance, **kwargs):
    from inventory.models import InventoryItem
    InventoryItem.objects.filter(product=instance).delete()