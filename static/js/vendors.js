// Load the Add Product modal dynamically
function loadAddProductModal(vendorId) {
    console.log('loadAddProductModal called with vendorId:', vendorId);
    fetch(`/vendors/add_product/${vendorId}/`)
        .then(response => {
            console.log('Fetch response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.text();
        })
        .then(html => {
            console.log('Fetched HTML:', html);
            // Inject the modal HTML into the DOM
            const modalContainer = document.createElement('div');
            modalContainer.innerHTML = html;
            document.body.appendChild(modalContainer);

            // Show the modal
            const modal = document.getElementById('addProductModal');
            if (modal) {
                console.log('Add Product modal found, displaying...');
                modal.style.display = 'block';

                // Set default value for quantity_supplied
                const quantityInput = document.getElementById('id_quantity_supplied');
                if (quantityInput) {
                    quantityInput.value = quantityInput.value || 0;
                }

                // Trigger initial calculation
                calculateTotalPriceAndDue();

                // Attach event listeners for live updates
                const modalForm = modal.querySelector('form');
                if (modalForm) {
                    modalForm.addEventListener('input', handleInput);
                }

                // Add click listener to close modal when clicking outside
                modal.addEventListener('click', function(event) {
                    if (event.target === modal) {
                        modal.style.display = 'none';
                        modal.remove(); // Clean up the DOM
                    }
                });

                // Ensure the close button works
                const closeBtn = modal.querySelector('.close-btn');
                if (closeBtn) {
                    closeBtn.addEventListener('click', function() {
                        modal.style.display = 'none';
                        modal.remove(); // Clean up the DOM
                    });
                }
            } else {
                console.error('Add Product modal not found in the loaded HTML');
            }
        })
        .catch(error => console.error('Error loading Add Product modal:', error));
}

// Load the Edit Product modal dynamically
function loadEditProductModal(productId, vendorId, productName, description, quantitySupplied, unitPrice, sellingPrice, totalPrice, dateOfOrder, paidAmount, dueAmount) {
    fetch(`/vendors/edit_product/${productId}/?vendor_id=${vendorId}`)
        .then(response => response.text())
        .then(html => {
            // Inject the modal HTML into the DOM
            const modalContainer = document.createElement('div');
            modalContainer.innerHTML = html;
            document.body.appendChild(modalContainer);

            // Populate the form fields
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

                // Attach event listeners for live updates
                const modalForm = modal.querySelector('form');
                if (modalForm) {
                    modalForm.addEventListener('input', handleInput);
                }

                // Add click listener to close modal when clicking outside
                modal.addEventListener('click', function(event) {
                    if (event.target === modal) {
                        modal.style.display = 'none';
                        modal.remove(); // Clean up the DOM
                    }
                });

                // Ensure the close button works
                const closeBtn = modal.querySelector('.close-btn');
                if (closeBtn) {
                    closeBtn.addEventListener('click', function() {
                        modal.style.display = 'none';
                        modal.remove(); // Clean up the DOM
                    });
                }
            } else {
                console.error('Edit Product modal or required elements not found in the loaded HTML');
            }
        })
        .catch(error => console.error('Error loading Edit Product modal:', error));
}

// Update the showEditProductForm function to use loadEditProductModal
function showEditProductForm(productId, productName, description, quantitySupplied, unitPrice, sellingPrice, totalPrice, dateOfOrder, paidAmount, dueAmount, vendorId) {
    loadEditProductModal(productId, vendorId, productName, description, quantitySupplied, unitPrice, sellingPrice, totalPrice, dateOfOrder, paidAmount, dueAmount);
}

// Add Product: Price calculation
function calculateTotalPriceAndDue() {
    var quantityInput = document.getElementById('id_quantity_supplied');
    var unitPriceInput = document.getElementById('id_unit_price');
    var sellingPriceInput = document.getElementById('id_selling_price');
    var paidAmountInput = document.getElementById('id_paid_amount');

    // Debug: Log the inputs to ensure they're found
    console.log('Calculating totals...');
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
        console.error('Display elements not found:', {
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
        console.error('Edit display elements not found:', {
            totalPriceDisplay: !!totalPriceDisplay,
            dueAmountDisplay: !!dueAmountDisplay
        });
    }
}

// Handle input events for both Add and Edit modals
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

// Event listener for search functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('productSearch');
    if (searchInput) {
        searchInput.addEventListener('keyup', searchProducts);
    }
});

// Other functions (for vendors_list.html, if needed)
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

function toggleAddVendorForm() {
    const form = document.getElementById('addVendorForm');
    if (form) {
        form.style.display = form.style.display === 'none' ? 'block' : 'none';
    }
}

function toggleEditVendorForm() {
    const form = document.getElementById('editVendorForm');
    if (form) {
        form.style.display = form.style.display === 'none' ? 'block' : 'none';
    }
}

function showEditVendorForm(vendorId, vendorName, address, contactNumber, dueAmount) {
    const form = document.getElementById('editVendorForm');
    const formAction = document.getElementById('editVendorFormAction');
    const vendorIdInput = document.getElementById('edit_vendor_id');
    const vendorNameInput = document.getElementById('edit_vendor_name');
    const addressInput = document.getElementById('edit_address');
    const contactNumberInput = document.getElementById('edit_contact_number');
    const dueAmountInput = document.getElementById('edit_due_amount');

    if (form && formAction && vendorIdInput && vendorNameInput && addressInput && contactNumberInput && dueAmountInput) {
        // Set the form action dynamically
        formAction.action = `/vendors/edit_vendor/${vendorId}/`;

        // Populate the form fields
        vendorIdInput.value = vendorId;
        vendorNameInput.value = vendorName;
        addressInput.value = address;
        contactNumberInput.value = contactNumber;
        dueAmountInput.value = dueAmount;

        // Show the form
        form.style.display = 'block';
    }
}

function confirmDelete() {
    return confirm("Are you sure you want to delete this vendor?");
}