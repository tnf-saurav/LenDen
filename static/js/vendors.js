// Add Product: Price calculation
function calculateTotalPriceAndDue() {
    var quantityInput = document.getElementById('id_quantity_supplied');
    var unitPriceInput = document.getElementById('id_unit_price');
    var sellingPriceInput = document.getElementById('id_selling_price');
    var paidAmountInput = document.getElementById('id_paid_amount');

    // Debug: Log the inputs to ensure they're found
    console.log('Calculating add totals...');
    console.log('Quantity:', quantityInput ? quantityInput.value : 'Not found');
    console.log('Unit Price:', unitPriceInput ? unitPriceInput.value : 'Not found');
    console.log('Paid Amount:', paidAmountInput ? paidAmountInput.value : 'Not found');

    // Enforce non-negative values
    function enforceNonNegative(input) {
        if (input && input.value < 0) {
            alert(`${input.name} cannot be negative. Setting to 0.`);
            input.value = 0;
        }
    }

    // Enforce integer values for quantity_supplied
    function enforceInteger(input) {
        if (input) {
            const value = parseFloat(input.value);
            if (isNaN(value)) {
                input.value = 0; // Silently reset to 0
            } else if (!Number.isInteger(value)) {
                const roundedValue = Math.round(value);
                alert(`${input.name} must be an integer. Rounding to ${roundedValue}.`);
                input.value = roundedValue;
            }
        }
    }

    // Apply validations
    enforceNonNegative(quantityInput);
    enforceNonNegative(unitPriceInput);
    enforceNonNegative(sellingPriceInput);
    enforceNonNegative(paidAmountInput);
    enforceInteger(quantityInput);

    // Calculate total_price and due_amount
    var quantity = parseInt(quantityInput ? quantityInput.value : 0) || 0;
    var unitPrice = parseFloat(unitPriceInput ? unitPriceInput.value : 0) || 0;
    var paidAmount = parseFloat(paidAmountInput ? paidAmountInput.value : 0) || 0;
    var totalPrice = quantity * unitPrice;
    var dueAmount = totalPrice - paidAmount;

    // Update the hidden input fields (for form submission)
    const totalPriceInput = document.getElementById('id_total_price');
    const dueAmountInput = document.getElementById('id_due_amount');
    if (totalPriceInput && dueAmountInput) {
        totalPriceInput.value = totalPrice.toFixed(2);
        dueAmountInput.value = dueAmount.toFixed(2);
    }

    // Update the display spans
    const totalPriceDisplay = document.getElementById('total_price_display');
    const dueAmountDisplay = document.getElementById('due_amount_display');
    if (totalPriceDisplay && dueAmountDisplay) {
        totalPriceDisplay.textContent = totalPrice.toFixed(2);
        dueAmountDisplay.textContent = dueAmount.toFixed(2);
    } else {
        console.error('Add Product display elements not found:', {
            totalPriceDisplay: !!totalPriceDisplay,
            dueAmountDisplay: !!dueAmountDisplay
        });
    }
}

// Edit Product: Price calculation
function calculateEditTotalPriceAndDue() {
    var quantityInput = document.getElementById('edit_quantity_supplied');
    var unitPriceInput = document.getElementById('edit_unit_price');
    var sellingPriceInput = document.getElementById('edit_selling_price');
    var paidAmountInput = document.getElementById('edit_paid_amount');

    // Debug: Log the inputs to ensure they're found
    console.log('Calculating edit totals...');
    console.log('Quantity:', quantityInput ? quantityInput.value : 'Not found');
    console.log('Unit Price:', unitPriceInput ? unitPriceInput.value : 'Not found');
    console.log('Paid Amount:', paidAmountInput ? paidAmountInput.value : 'Not found');

    // Enforce non-negative values
    function enforceNonNegative(input) {
        if (input && input.value < 0) {
            alert(`${input.name} cannot be negative. Setting to 0.`);
            input.value = 0;
        }
    }

    // Enforce integer values for quantity_supplied
    function enforceInteger(input) {
        if (input) {
            const value = parseFloat(input.value);
            if (isNaN(value)) {
                input.value = 0; // Silently reset to 0
            } else if (!Number.isInteger(value)) {
                const roundedValue = Math.round(value);
                alert(`${input.name} must be an integer. Rounding to ${roundedValue}.`);
                input.value = roundedValue;
            }
        }
    }

    // Apply validations
    enforceNonNegative(quantityInput);
    enforceNonNegative(unitPriceInput);
    enforceNonNegative(sellingPriceInput);
    enforceNonNegative(paidAmountInput);
    enforceInteger(quantityInput);

    // Calculate total_price and due_amount
    var quantity = parseInt(quantityInput ? quantityInput.value : 0) || 0;
    var unitPrice = parseFloat(unitPriceInput ? unitPriceInput.value : 0) || 0;
    var paidAmount = parseFloat(paidAmountInput ? paidAmountInput.value : 0) || 0;
    var totalPrice = quantity * unitPrice;
    var dueAmount = totalPrice - paidAmount;

    // Update the hidden input fields (for form submission)
    const totalPriceInput = document.getElementById('edit_total_price');
    const dueAmountInput = document.getElementById('edit_due_amount');
    if (totalPriceInput && dueAmountInput) {
        totalPriceInput.value = totalPrice.toFixed(2);
        dueAmountInput.value = dueAmount.toFixed(2);
    }

    // Update the display spans
    const totalPriceDisplay = document.getElementById('edit_total_price_display');
    const dueAmountDisplay = document.getElementById('edit_due_amount_display');
    if (totalPriceDisplay && dueAmountDisplay) {
        totalPriceDisplay.textContent = totalPrice.toFixed(2);
        dueAmountDisplay.textContent = dueAmount.toFixed(2);
    } else {
        console.error('Edit Product display elements not found:', {
            totalPriceDisplay: !!totalPriceDisplay,
            dueAmountDisplay: !!dueAmountDisplay
        });
    }
}

// Show the Add Product modal
function showAddProductModal() {
    console.log('showAddProductModal called');
    const modal = document.getElementById('addProductModal');
    if (modal) {
        console.log('Add Product modal found');
        // Reset the form
        const form = modal.querySelector('form');
        if (form) {
            console.log('Add Product form found');
            form.reset();
            // Reset calculated values
            const totalPriceDisplay = document.getElementById('total_price_display');
            const dueAmountDisplay = document.getElementById('due_amount_display');
            if (totalPriceDisplay && dueAmountDisplay) {
                totalPriceDisplay.textContent = '0.00';
                dueAmountDisplay.textContent = '0.00';
            }
            // Set default value for quantity_supplied
            const quantityInput = document.getElementById('id_quantity_supplied');
            if (quantityInput) {
                quantityInput.value = 0;
            }
            // Clear any existing form errors
            const errorElements = modal.querySelectorAll('.form-error');
            errorElements.forEach(element => {
                element.innerHTML = '';
            });
        } else {
            console.error('Add Product form not found');
        }
        modal.style.display = 'block';
        calculateTotalPriceAndDue();
    } else {
        console.error('Add Product modal not found');
    }
}

// Show and populate the Edit Product form
function showEditProductForm(productId, productName, description, quantitySupplied, unitPrice, sellingPrice, totalPrice, dateOfOrder, paidAmount, dueAmount, vendorId) {
    console.log('showEditProductForm called with:', { productId, productName, description, quantitySupplied, unitPrice, sellingPrice, totalPrice, dateOfOrder, paidAmount, dueAmount, vendorId });
    const modal = document.getElementById('editProductModal');
    const form = document.getElementById('editProductForm');
    const productIdInput = document.getElementById('edit_product_id');
    const productNameInput = document.getElementById('edit_product_name');
    const descriptionInput = document.getElementById('edit_description');
    const quantitySuppliedInput = document.getElementById('edit_quantity_supplied');
    const unitPriceInput = document.getElementById('edit_unit_price');
    const sellingPriceInput = document.getElementById('edit_selling_price');
    const totalPriceInput = document.getElementById('edit_total_price');
    const totalPriceDisplay = document.getElementById('edit_total_price_display');
    const dateOfOrderInput = document.getElementById('edit_date_of_order');
    const paidAmountInput = document.getElementById('edit_paid_amount');
    const dueAmountInput = document.getElementById('edit_due_amount');
    const dueAmountDisplay = document.getElementById('edit_due_amount_display');

    if (modal && form && productIdInput && productNameInput && descriptionInput && quantitySuppliedInput && unitPriceInput && sellingPriceInput && totalPriceInput && totalPriceDisplay && dateOfOrderInput && paidAmountInput && dueAmountInput && dueAmountDisplay) {
        console.log('All Edit Product elements found');
        // Set the form action dynamically
        form.action = `/vendors/edit_product/${productId}/?vendor_id=${vendorId}`;

        // Populate the form fields
        productIdInput.value = productId;
        productNameInput.value = productName;
        descriptionInput.value = description;
        quantitySuppliedInput.value = quantitySupplied;
        unitPriceInput.value = unitPrice;
        sellingPriceInput.value = sellingPrice;
        totalPriceInput.value = totalPrice;
        totalPriceDisplay.textContent = parseFloat(totalPrice).toFixed(2);
        dateOfOrderInput.value = dateOfOrder;
        paidAmountInput.value = paidAmount;
        dueAmountInput.value = dueAmount;
        dueAmountDisplay.textContent = parseFloat(dueAmount).toFixed(2);

        // Show the modal
        modal.style.display = 'block';

        // Trigger initial calculation
        calculateEditTotalPriceAndDue();
    } else {
        console.error('Edit Product modal or required elements not found', {
            modal: !!modal,
            form: !!form,
            productIdInput: !!productIdInput,
            productNameInput: !!productNameInput,
            descriptionInput: !!descriptionInput,
            quantitySuppliedInput: !!quantitySuppliedInput,
            unitPriceInput: !!unitPriceInput,
            sellingPriceInput: !!sellingPriceInput,
            totalPriceInput: !!totalPriceInput,
            totalPriceDisplay: !!totalPriceDisplay,
            dateOfOrderInput: !!dateOfOrderInput,
            paidAmountInput: !!paidAmountInput,
            dueAmountInput: !!dueAmountInput,
            dueAmountDisplay: !!dueAmountDisplay
        });
    }
}

// Show the Add Vendor modal
function showAddVendorModal() {
    console.log('showAddVendorModal called');
    const modal = document.getElementById('addVendorModal');
    if (modal) {
        console.log('Add Vendor modal found');
        // Reset the form
        const form = modal.querySelector('form');
        if (form) {
            console.log('Add Vendor form found');
            form.reset();
            // Set default value for due_amount
            const dueAmountInput = document.getElementById('id_due_amount');
            if (dueAmountInput) {
                dueAmountInput.value = '0.00';
            }
            // Clear any existing form errors
            const errorElements = modal.querySelectorAll('.form-error');
            errorElements.forEach(element => {
                element.innerHTML = '';
            });
        } else {
            console.error('Add Vendor form not found');
        }
        modal.style.display = 'block';
    } else {
        console.error('Add Vendor modal not found');
    }
}

// Show and populate the Edit Vendor form
function showEditVendorForm(vendorId, vendorName, address, contactNumber, dueAmount) {
    console.log('showEditVendorForm called with:', { vendorId, vendorName, address, contactNumber, dueAmount });
    const modal = document.getElementById('editVendorModal');
    const form = document.getElementById('editVendorForm');
    const vendorIdInput = document.getElementById('edit_vendor_id');
    const vendorNameInput = document.getElementById('edit_vendor_name');
    const addressInput = document.getElementById('edit_address');
    const contactNumberInput = document.getElementById('edit_contact_number');
    const dueAmountInput = document.getElementById('edit_due_amount');

    if (modal && form && vendorIdInput && vendorNameInput && addressInput && contactNumberInput && dueAmountInput) {
        console.log('All Edit Vendor elements found');
        // Set the form action dynamically
        form.action = `/vendors/edit_vendor/${vendorId}/`;

        // Populate the form fields
        vendorIdInput.value = vendorId;
        vendorNameInput.value = vendorName;
        addressInput.value = address;
        contactNumberInput.value = contactNumber;
        dueAmountInput.value = dueAmount;

        // Show the modal
        modal.style.display = 'block';
    } else {
        console.error('Edit Vendor modal or required elements not found', {
            modal: !!modal,
            form: !!form,
            vendorIdInput: !!vendorIdInput,
            vendorNameInput: !!vendorNameInput,
            addressInput: !!addressInput,
            contactNumberInput: !!contactNumberInput,
            dueAmountInput: !!dueAmountInput
        });
    }
}

// Handle input events for both Add and Edit Product modals
function handleInput(event) {
    const target = event.target;
    if (target.matches('#id_quantity_supplied, #id_unit_price, #id_selling_price, #id_paid_amount')) {
        calculateTotalPriceAndDue();
    } else if (target.matches('#edit_quantity_supplied, #edit_unit_price, #edit_selling_price, #edit_paid_amount')) {
        calculateEditTotalPriceAndDue();
    }
}

// vendors_detail.html: Search products
function searchProducts() {
    let input = document.getElementById("productSearch").value.toLowerCase();
    
    let productRows = document.querySelectorAll(".products-table .table-row");

    productRows.forEach(row => {
        let rowText = row.textContent.toLowerCase();
        
        if (rowText.includes(input)) {
            row.style.display = "flex";
        } else {
            row.style.display = "none"; 
        }
    });
}

// vendors_detail.html: Delete product via fetch
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
        })
        .catch(error => console.error('Error deleting product:', error));
    }
}

// vendors_list.html: Search vendors
function searchVendors() {
    const input = document.getElementById('vendorSearch').value.trim().toLowerCase();
    const rows = document.querySelectorAll('.table-row');
    rows.forEach(row => {
        const vendorNameElement = row.querySelector('.vendor-details .table-col:nth-child(1)');
        const addressElement = row.querySelector('.vendor-details .table-col:nth-child(2)');

        const vendorName = vendorNameElement ? vendorNameElement.textContent.trim().toLowerCase() : '';
        const address = addressElement ? addressElement.textContent.trim().toLowerCase() : '';

        if (vendorName.includes(input) || address.includes(input)) {   
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Utility function to get CSRF token
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

// Event listener for search functionality and modal interactions
document.addEventListener('DOMContentLoaded', function() {
    // Search functionality for products (vendors_detail.html)
    const searchInput = document.getElementById('productSearch');
    if (searchInput) {
        searchInput.addEventListener('keyup', searchProducts);
    }

    // Search functionality for vendors (vendors_list.html)
    const vendorSearchInput = document.getElementById('vendorSearch');
    if (vendorSearchInput) {
        vendorSearchInput.addEventListener('keyup', searchVendors);
    }

    // Attach input event listeners to Add Product modal
    const addProductForm = document.querySelector('#addProductModal form');
    if (addProductForm) {
        console.log('Add Product form found on page load');
        addProductForm.addEventListener('input', handleInput);
    } else {
        console.error('Add Product form not found on page load');
    }

    // Attach input event listeners to Edit Product modal
    const editProductForm = document.querySelector('#editProductModal form');
    if (editProductForm) {
        console.log('Edit Product form found on page load');
        editProductForm.addEventListener('input', handleInput);
    } else {
        console.error('Edit Product form not found on page load');
    }

    // Add click listener to close modals when clicking outside
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('click', function(event) {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    });

    // Add click listener to close modals when clicking the close button
    const closeButtons = document.querySelectorAll('.close-btn');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const modal = button.closest('.modal');
            if (modal) {
                modal.style.display = 'none';
            }
        });
    });
});

// vendors_list.html: Confirm delete
function confirmDelete() {
    return confirm("Are you sure you want to delete this vendor?");
}