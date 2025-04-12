"""
URL configuration for lenden project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from authentication.accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', account_views.home, name='dashboard'),
    path('', include('authentication.accounts.urls')),
    path('accounts/', include('authentication.accounts.urls')),
    path('vendors/', include('authentication.vendors.urls')),
    path('inventory/', include('authentication.inventory.urls')),
    path('customers/', include('authentication.customers.urls')),
    # path('invoice/', include('authentication.invoice.urls')),
    # path('sales/', include('authentication.sales.urls')),
    path('dashboard/', include('authentication.dashboard.urls')),
]
