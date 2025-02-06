from mongoengine import Document, EmbeddedDocument, StringField, BooleanField, DateTimeField, FloatField, ListField, EmbeddedDocumentField
from datetime import datetime

# Define product details for each vendor
class Product(EmbeddedDocument):
    product_name = StringField(required=True)
    description = StringField()
    quantity_supplied = FloatField(required=True)
    unit_price = FloatField(required=True)
    total_price = FloatField(required=True)
    date_of_order = DateTimeField(required=True)

# Define Vendor document
class Vendor(Document):
    vendor_name = StringField(required=True)
    address = StringField()
    contact_number = StringField()
    due_amount = FloatField(default=0.0)
    advance_paid = FloatField(default=0.0)
    products = ListField(EmbeddedDocumentField(Product))
    is_due = BooleanField(default=False)  # Red or Green dot based on this status
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'vendors'  # Define the collection name
    }