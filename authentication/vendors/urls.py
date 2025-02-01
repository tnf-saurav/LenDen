from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('vendors_list/', views.vendors_list, name='vendors_list'),
    path('vendors_detail/', views.vendors_detail, name='vendors_detail'),
]