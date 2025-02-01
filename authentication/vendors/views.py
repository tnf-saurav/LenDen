from django.shortcuts import render
from .models import Vendor
from django.db.models import Q

# Create your views here.

def home(request):
    return render(request, "index.html")

def vendors_list(request):
    query = request.GET.get('search', '')
    if query:
        vendors = Vendor.objects.filter(
            Q(vendor_name__icontains=query) |
            Q(address__icontains=query)
        )
    else:
        vendors = Vendor.objects.all()
    
    return render(request, 'vendors/vendors_list.html', {'vendors': vendors})

def vendors_detail(request, vendor_id):
    # Logic for displaying a single vendor's detail
    vendor = get_object_or_404(Vendor, id=vendor_id)
    
    return render(request, 'vendors/vendors_detail.html', {'vendor': vendor})