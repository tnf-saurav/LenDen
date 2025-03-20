// static/js/vendors.js

// add_product.html: Price calculation
function calculateTotalPriceAndDue() {
    var quantity = parseFloat(document.getElementById('id_quantity_supplied').value) || 0;
    var unitPrice = parseFloat(document.getElementById('id_unit_price').value) || 0;
    var paidAmount = parseFloat(document.getElementById('id_paid_amount').value) || 0;
    var totalPrice = quantity * unitPrice;
    var dueAmount = totalPrice - paidAmount;
    document.getElementById('id_total_price').value = totalPrice.toFixed(2);
    document.getElementById('id_due_amount').value = Math.abs(dueAmount).toFixed(2);
}

// vendors_detail.html: Search products
function searchProducts() {
    var input = document.getElementById('productSearch');
    var filter = input.value.toLowerCase();
    var productBoxes = document.getElementsByClassName('product-box');
    for (var i = 0; i < productBoxes.length; i++) {
        var txtValue = productBoxes[i].textContent || productBoxes[i].innerText;
        if (txtValue.toLowerCase().indexOf(filter) > -1) {
            productBoxes[i].style.display = "";
        } else {
            productBoxes[i].style.display = "none";
        }
    }
}

// vendors_detail.html: Delete product via fetch (commented out, but included for completeness)
function deleteProduct(productId, vendorId) {
    if (confirm('Are you sure you want to delete this product?')) {
        fetch(`/vendors/delete_product/${productId}/?vendor_id=${vendorId}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        })
        .then(response => {
            if (response.ok) {
                document.getElementById(`product-${productId}`).remove();
            } else {
                alert('Failed to delete the product.');
            }
        });
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// jQuery setup for add_product.html
$(document).ready(function() {
    $('#id_quantity_supplied, #id_unit_price, #id_paid_amount').on('input', function() {
        calculateTotalPriceAndDue();
    });
});

// static/js/vendors.js
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('vendorSearch');
    if (searchInput) {
        searchInput.addEventListener('keyup', searchVendors);
    }
});

function searchVendors() {
    const input = document.getElementById('vendorSearch').value.toLowerCase();
    const rows = document.querySelectorAll('.table-row');
    rows.forEach(row => {
        const vendorName = row.querySelector('.table-col:nth-child(2)').textContent.toLowerCase();
        const address = row.querySelector('.table-col:nth-child(3)').textContent.toLowerCase();
        if (vendorName.includes(input) || address.includes(input)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}
