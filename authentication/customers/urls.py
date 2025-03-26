from django.urls import path
from . import views

urlpatterns = [
    path('', views.customers_list, name='customers_list'),
    path('customer/<int:customer_id>/', views.customers_detail, name='customers_detail'),
    path('add/', views.customers_list, name='add_customer'),
]