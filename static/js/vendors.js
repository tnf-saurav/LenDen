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

// Generic function to calculate total price and due amount
function calculatePriceAndDue(prefix = 'id') {
    const quantityInput = document.getElementById(`${prefix}_quantity_supplied`);
    const unitPriceInput = document.getElementById(`${prefix}_unit_price`);
    const sellingPriceInput = document.getElementById(`${prefix}_selling_price`);
    const paidAmountInput = document.getElementById(`${prefix}_paid_amount`);

    console.log(`Calculating totals for ${prefix}...`);
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
                input.value = 0;
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
    const quantity = parseInt(quantityInput ? quantityInput.value : 0) || 0;
    const unitPrice = parseFloat(unitPriceInput ? unitPriceInput.value : 0) || 0;
    const paidAmount = parseFloat(paidAmountInput ? paidAmountInput.value : 0) || 0;
    const totalPrice = quantity * unitPrice;
    const dueAmount = totalPrice - paidAmount;

    // Update the hidden input fields
    const totalPriceInput = document.getElementById(`${prefix}_total_price`);
    const dueAmountInput = document.getElementById(`${prefix}_due_amount`);
    if (totalPriceInput && dueAmountInput) {
        totalPriceInput.value = totalPrice.toFixed(2);
        dueAmountInput.value = dueAmount.toFixed(2);
    }

    // Update the display spans
    const totalPriceDisplay = document.getElementById(`${prefix}_total_price_display`);
    const dueAmountDisplay = document.getElementById(`${prefix}_due_amount_display`);
    if (totalPriceDisplay && dueAmountDisplay) {
        totalPriceDisplay.textContent = totalPrice.toFixed(2);
        dueAmountDisplay.textContent = dueAmount.toFixed(2);
    } else {
        console.error(`${prefix} Product display elements not found:`, {
            totalPriceDisplay: !!totalPriceDisplay,
            dueAmountDisplay: !!dueAmountDisplay
        });
    }
}

// Generic function to reset a modal form
function resetModalForm(modal, defaultValues = {}) {
    console.log('Resetting modal form...');
    const form = modal.querySelector('form');
    if (form) {
        form.reset();
        // Set default values
        Object.keys(defaultValues).forEach(id => {
            const input = document.getElementById(id);
            if (input) {
                input.value = defaultValues[id];
            }
        });
        // Clear form errors
        const errorElements = modal.querySelectorAll('.form-error');
        errorElements.forEach(element => {
            element.innerHTML = '';
        });
    } else {
        console.error('Form not found in modal');
    }
}

// Show the Add Vendor modal
function showAddVendorModal() {
    console.log('showAddVendorModal called');
    const modal = document.getElementById('addVendorModal');
    if (modal) {
        resetModalForm(modal, { 'id_due_amount': '0.00' });
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
    const elements = {
        vendorIdInput: document.getElementById('edit_vendor_id'),
        vendorNameInput: document.getElementById('edit_vendor_name'),
        addressInput: document.getElementById('edit_address'),
        contactNumberInput: document.getElementById('edit_contact_number'),
        dueAmountInput: document.getElementById('edit_due_amount')
    };

    if (modal && form && Object.values(elements).every(el => el)) {
        form.action = `/vendors/edit_vendor/${vendorId}/`;
        elements.vendorIdInput.value = vendorId;
        elements.vendorNameInput.value = vendorName;
        elements.addressInput.value = address;
        elements.contactNumberInput.value = contactNumber;
        elements.dueAmountInput.value = dueAmount;
        modal.style.display = 'block';
    } else {
        console.error('Edit Vendor modal or required elements not found', {
            modal: !!modal,
            form: !!form,
            ...Object.fromEntries(Object.entries(elements).map(([key, value]) => [key, !!value]))
        });
    }
}

// Show the Add Product modal
function showAddProductModal() {
    console.log('showAddProductModal called');
    const modal = document.getElementById('addProductModal');
    if (modal) {
        resetModalForm(modal, { 'id_quantity_supplied': '0' });
        modal.style.display = 'block';
        calculatePriceAndDue('id');
    } else {
        console.error('Add Product modal not found');
    }
}

// Show and populate the Edit Product form
function showEditProductForm(productId, productName, description, quantitySupplied, unitPrice, sellingPrice, totalPrice, dateOfOrder, paidAmount, dueAmount, vendorId) {
    console.log('showEditProductForm called with:', { productId, productName, description, quantitySupplied, unitPrice, sellingPrice, totalPrice, dateOfOrder, paidAmount, dueAmount, vendorId });
    const modal = document.getElementById('editProductModal');
    const form = document.getElementById('editProductForm');
    const elements = {
        productIdInput: document.getElementById('edit_product_id'),
        productNameInput: document.getElementById('edit_product_name'),
        descriptionInput: document.getElementById('edit_description'),
        quantitySuppliedInput: document.getElementById('edit_quantity_supplied'),
        unitPriceInput: document.getElementById('edit_unit_price'),
        sellingPriceInput: document.getElementById('edit_selling_price'),
        totalPriceInput: document.getElementById('edit_total_price'),
        totalPriceDisplay: document.getElementById('edit_total_price_display'),
        dateOfOrderInput: document.getElementById('edit_date_of_order'),
        paidAmountInput: document.getElementById('edit_paid_amount'),
        dueAmountInput: document.getElementById('edit_due_amount'),
        dueAmountDisplay: document.getElementById('edit_due_amount_display')
    };

    if (modal && form && Object.values(elements).every(el => el)) {
        form.action = `/vendors/edit_product/${productId}/?vendor_id=${vendorId}`;
        elements.productIdInput.value = productId;
        elements.productNameInput.value = productName;
        elements.descriptionInput.value = description;
        elements.quantitySuppliedInput.value = quantitySupplied;
        elements.unitPriceInput.value = unitPrice;
        elements.sellingPriceInput.value = sellingPrice;
        elements.totalPriceInput.value = totalPrice;
        elements.totalPriceDisplay.textContent = parseFloat(totalPrice).toFixed(2);
        elements.dateOfOrderInput.value = dateOfOrder;
        elements.paidAmountInput.value = paidAmount;
        elements.dueAmountInput.value = dueAmount;
        elements.dueAmountDisplay.textContent = parseFloat(dueAmount).toFixed(2);
        modal.style.display = 'block';
        calculatePriceAndDue('edit');
    } else {
        console.error('Edit Product modal or required elements not found', {
            modal: !!modal,
            form: !!form,
            ...Object.fromEntries(Object.entries(elements).map(([key, value]) => [key, !!value]))
        });
    }
}

// Generic search function for tables
function searchTable(searchInputId, rowSelector, getSearchText) {
    const input = document.getElementById(searchInputId).value.trim().toLowerCase();
    const rows = document.querySelectorAll(rowSelector);
    rows.forEach(row => {
        const text = getSearchText(row).toLowerCase();
        row.style.display = text.includes(input) ? '' : 'none';
    });
}

// vendors_list.html: Search vendors
function searchVendors() {
    searchTable('vendorSearch', '.table-row', row => {
        const vendorNameElement = row.querySelector('.vendor-details .table-col:nth-child(1)');
        const addressElement = row.querySelector('.vendor-details .table-col:nth-child(2)');
        const vendorName = vendorNameElement ? vendorNameElement.textContent.trim() : '';
        const address = addressElement ? addressElement.textContent.trim() : '';
        return `${vendorName} ${address}`;
    });
}

// vendors_detail.html: Search products
function searchProducts() {
    searchTable('productSearch', '.products-table .table-row', row => row.textContent.trim());
}

// vendors_list.html: Confirm delete
function confirmDelete() {
    return confirm("Are you sure you want to delete this vendor?");
}

// Handle input events for both Add and Edit Product modals
function handleInput(event) {
    const target = event.target;
    if (target.matches('#id_quantity_supplied, #id_unit_price, #id_selling_price, #id_paid_amount')) {
        calculatePriceAndDue('id');
    } else if (target.matches('#edit_quantity_supplied, #edit_unit_price, #edit_selling_price, #edit_paid_amount')) {
        calculatePriceAndDue('edit');
    }
}

// Event listener for DOM content loaded
document.addEventListener('DOMContentLoaded', function() {
    // Search functionality
    const searchInput = document.getElementById('productSearch');
    if (searchInput) {
        searchInput.addEventListener('keyup', searchProducts);
    }

    const vendorSearchInput = document.getElementById('vendorSearch');
    if (vendorSearchInput) {
        vendorSearchInput.addEventListener('keyup', searchVendors);
    }

    // Attach input event listeners to Add and Edit Product modals
    const addProductForm = document.querySelector('#addProductModal form');
    if (addProductForm) {
        addProductForm.addEventListener('input', handleInput);
    }

    const editProductForm = document.querySelector('#editProductModal form');
    if (editProductForm) {
        editProductForm.addEventListener('input', handleInput);
    }

    // Modal interactions
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('click', function(event) {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    });

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