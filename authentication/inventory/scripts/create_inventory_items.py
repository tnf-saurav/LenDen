from authentication.vendors.models import Product
from authentication.inventory.models import InventoryItem

# Example products
products = Product.objects.all()

# Create InventoryItem instances for each product
for product in products:
    InventoryItem.objects.create(
        product=product,
        remaining_quantity=product.quantity_supplied,  # or any other logic to determine remaining quantity
        selling_price=product.selling_price  # or any other logic to determine selling price
    )