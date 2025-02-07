from django.urls import path
from .views import vendors_list, add_vendor, vendors_detail, add_product

urlpatterns = [
    path('vendors_list/', vendors_list, name='vendors_list'),
    path('add/', add_vendor, name='add_vendor'),
    path('<str:vendor_id>/', vendors_detail, name='vendors_detail'),
    path('<str:vendor_id>/add_product/', add_product, name='add_product'),
]