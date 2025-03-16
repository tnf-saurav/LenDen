from django.urls import path
from . import views

# urlpatterns = [
#     path('vendors_list/', vendors_list, name='vendors_list'),
#     path('add/', add_vendor, name='add_vendor'),
#     path('<str:vendor_id>/', vendors_detail, name='vendors_detail'),
#     path('<str:vendor_id>/add_product/', add_product, name='add_product'),
# ]

urlpatterns = [
    path('', views.vendors_list, name='vendors_list'),
    path('vendor/<int:vendor_id>/', views.vendors_detail, name='vendors_detail'),
    path('add_vendor/', views.add_vendor, name='add_vendor'),
    path('edit_vendor/<int:vendor_id>/', views.edit_vendor, name='edit_vendor'),
    path('delete_vendor/<int:vendor_id>/', views.delete_vendor, name='delete_vendor'),
    path('add_product/<int:vendor_id>/', views.add_product, name='add_product'),
    path('edit_product/<uuid:product_id>/', views.edit_product, name='edit_product'), 
    path('delete_product/<uuid:product_id>/', views.delete_product, name='delete_product'),
    path('pay/<int:vendor_id>/', views.pay_vendor, name='pay_vendor'),
    path('download_statement/<int:vendor_id>/', views.download_statement, name='download_statement'),
]