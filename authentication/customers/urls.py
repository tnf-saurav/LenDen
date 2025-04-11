from django.urls import path
from . import views

urlpatterns = [
    path('', views.customers_list, name='customers_list'),
    path('customer/<int:customer_id>/', views.customers_detail, name='customers_detail'),
    path('add/', views.customers_list, name='add_customer'),
    path('customer/<int:customer_id>/invoice/', views.create_invoice, name='create_invoice'),
    path('customer/<int:customer_id>/invoice/<int:invoice_id>/edit/', views.edit_invoice, name='edit_invoice'),
    path('product-autocomplete/', views.product_autocomplete, name='product_autocomplete'),
    path('customer/<int:customer_id>/pay/', views.pay_customer, name='pay_customer'),
]