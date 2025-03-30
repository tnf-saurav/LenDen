// Modal Functionality
const addCustomerModal = document.getElementById("addCustomerModal");
const editCustomerModal = document.getElementById("editCustomerModal");
const createInvoiceModal = document.getElementById("createInvoiceModal");
const addCustomerBtn = document.querySelector(".add-customer-btn");
const closeButtons = document.querySelectorAll(".close-btn");

// Show Add Customer Modal
function showAddCustomerModal() {
    addCustomerModal.style.display = "block";
}

// Show Edit Customer Modal
function showEditCustomerForm(customerId, customerName, address, contactNumber, dueAmount) {
    document.getElementById("edit_customer_id").value = customerId;
    document.getElementById("edit_customer_name").value = customerName;
    document.getElementById("edit_address").value = address;
    document.getElementById("edit_contact_number").value = contactNumber;
    document.getElementById("edit_due_amount").value = dueAmount;
    editCustomerModal.style.display = "block";
}

function showCreateInvoiceModal() {
    document.getElementById('createInvoiceModal').style.display = 'block';
}

function closeCreateInvoiceModal() {
    document.getElementById('createInvoiceModal').style.display = 'none';
}

// Close Modals
closeButtons.forEach(button => {
    button.addEventListener("click", () => {
        addCustomerModal.style.display = "none";
        editCustomerModal.style.display = "none";
        createInvoiceModal.style.display = "none";
    });
});

// Close modal when clicking outside
window.addEventListener("click", (event) => {
    if (event.target === addCustomerModal) {
        addCustomerModal.style.display = "none";
    }
    if (event.target === editCustomerModal) {
        editCustomerModal.style.display = "none";
    }
    if (event.target === createInvoiceModal) {
        createInvoiceModal.style.display = "none";
    }
});

// Confirm Delete
function confirmDelete() {
    return confirm("Are you sure you want to delete this customer?");
}

// Search Functionality
function searchCustomers() {
    let input = document.getElementById("customerSearch").value.toLowerCase();
    let rows = document.querySelectorAll(".table-body .table-row");
    let hasVisibleRows = false;

    rows.forEach(row => {
        let isEmptyRow = row.querySelector(".table-col")?.textContent.includes("No customers found");
        if (isEmptyRow) {
            row.style.display = "none";
            return;
        }

        let customerName = row.querySelector(".table-col:nth-child(1)").textContent.toLowerCase();
        if (customerName.includes(input)) {
            row.style.display = "flex";
            hasVisibleRows = true;
        } else {
            row.style.display = "none";
        }
    });

    if (!hasVisibleRows) {
        let emptyRow = Array.from(rows).find(row => 
            row.querySelector(".table-col")?.textContent.includes("No customers found")
        );
        if (emptyRow) {
            emptyRow.style.display = "flex";
        }
    }
}

// Invoice Functionality
$(document).ready(function() {
    // Autocomplete for products
    function initializeAutocomplete() {
        $('.product-autocomplete').each(function() {
            $(this).autocomplete({
                source: productAutocompleteUrl,
                minLength: 1,
                select: function(event, ui) {
                    // Set the hidden product field with the selected product's ID
                    $(this).siblings('input[type="hidden"]').val(ui.item.id);
                    console.log('Selected product ID:', ui.item.id);  // Debug log
                    console.log('Hidden input value:', $(this).siblings('input[type="hidden"]').val());  // Debug log
                    calculateTotal();
                },
                open: function() {
                    console.log("Autocomplete opened");
                },
                error: function(xhr, status, error) {
                    console.error("Autocomplete error:", status, error);
                }
            });
        });
    }

    // Initialize autocomplete on page load
    initializeAutocomplete();

    $('#add-item').click(function() {
        console.log('Add Product button clicked');
        let formIdx = parseInt($('#id_items-TOTAL_FORMS').val());
        console.log('Current form index:', formIdx);
        console.log('Item rows found:', $('.item-row').length);  // Debug log
    
        // Clone the first item row
        let newRow = $('.item-row:first').clone(true);
        if (!newRow.length) {
            console.error("No item row found to clone");
            return;
        }
    
        // Update the names and IDs of the inputs in the new row
        newRow.find('input').each(function() {
            let name = $(this).attr('name');
            if (name) {
                $(this).attr('name', name.replace('-0-', '-' + formIdx + '-'));
            }
            let id = $(this).attr('id');
            if (id) {
                $(this).attr('id', id.replace('-0-', '-' + formIdx + '-'));
            }
            // Clear input values
            if ($(this).hasClass('product-autocomplete')) {
                $(this).val('');  // Clear product_name
            } else if ($(this).attr('name').includes('product')) {
                $(this).val('');  // Clear hidden product field
            } else {
                $(this).val('');
            }
        });
    
        // Reset the total price display
        newRow.find('.total-price').val('0.00');
    
        // Append the new row and update the formset total forms
        $('#item-formset').append(newRow);
        $('#id_items-TOTAL_FORMS').val(formIdx + 1);
    
        // Reinitialize autocomplete for the new row
        initializeAutocomplete();
        calculateTotal();
    });
    
    // Remove item row
    $(document).on('click', '.remove-item', function() {
        if ($('.item-row').length > 1) {
            $(this).closest('.item-row').remove();
            calculateTotal();
        } else {
            // Allow removing the last item row, but validate on form submission
            $(this).closest('.item-row').remove();
            calculateTotal();
        }
    });

    // Add service row
    $('#add-service').click(function() {
        console.log('Add Service button clicked');
        let formIdx = parseInt($('#id_services-TOTAL_FORMS').val());
        console.log('Current service form index:', formIdx);

        // Clone the first service row
        let newRow = $('.service-row:first').clone(true);
        if (!newRow.length) {
            console.error("No service row found to clone");
            return;
        }

        // Update the names and IDs of the inputs in the new row
        newRow.find('input').each(function() {
            let name = $(this).attr('name');
            if (name) {
                $(this).attr('name', name.replace('-0-', '-' + formIdx + '-'));
            }
            let id = $(this).attr('id');
            if (id) {
                $(this).attr('id', id.replace('-0-', '-' + formIdx + '-'));
            }
            $(this).val('');  // Clear input values
        });

        // Append the new row and update the formset total forms
        $('#service-formset').append(newRow);
        $('#id_services-TOTAL_FORMS').val(formIdx + 1);
        calculateTotal();
    });

    // Remove service row
    $(document).on('click', '.remove-service', function() {
        if ($('.service-row').length > 1) {
            $(this).closest('.service-row').remove();
            calculateTotal();
        } else {
            // Allow removing the last service row, but validate on form submission
            $(this).closest('.service-row').remove();
            calculateTotal();
        }
    });

    // Calculate totals on input change
    $(document).on('input', 'input[name$="quantity"], input[name$="unit_price"], input[name$="price"], #id_discount_percent, #id_discount_amount', calculateTotal);

    // Function to calculate totals
    function calculateTotal() {
        let total = 0;

        // Calculate total for items
        $('.item-row').each(function() {
            let qty = parseFloat($(this).find('input[name$="quantity"]').val()) || 0;
            let price = parseFloat($(this).find('input[name$="unit_price"]').val()) || 0;
            let itemTotal = qty * price;
            $(this).find('.total-price').val(itemTotal.toFixed(2));
            total += itemTotal;
        });

        // Calculate total for services
        $('.service-row').each(function() {
            let price = parseFloat($(this).find('input[name$="price"]').val()) || 0;
            total += price;
        });

        // Update subtotal
        $('#total-amount').val(total.toFixed(2));

        // Calculate discount
        let discountPercent = parseFloat($('#id_discount_percent').val()) || 0;
        let discountAmount = parseFloat($('#id_discount_amount').val()) || 0;
        if (discountPercent > 0) {
            discountAmount = total * (discountPercent / 100);
            $('#id_discount_amount').val(discountAmount.toFixed(2));
        } else if (discountAmount > 0) {
            discountPercent = (discountAmount / total) * 100;
            $('#id_discount_percent').val(discountPercent.toFixed(2));
        }

        // Update final amount
        let finalAmount = total - discountAmount;
        $('#final-amount').val(finalAmount.toFixed(2));
    }

    // Validate form on submission
    $('#invoiceForm').on('submit', function(event) {
        let itemRows = $('.item-row');
        let serviceRows = $('.service-row');
        let hasItems = false;
        let hasServices = false;

        // Check if there are any items with a selected product
        itemRows.each(function() {
            let productId = $(this).find('input[name$="product"]').val();
            let quantity = parseFloat($(this).find('input[name$="quantity"]').val()) || 0;
            if (productId && quantity > 0) {
                hasItems = true;
            }
        });

        // Check if there are any services with a price
        serviceRows.each(function() {
            let price = parseFloat($(this).find('input[name$="price"]').val()) || 0;
            if (price > 0) {
                hasServices = true;
            }
        });

        // Require at least one item or one service
        if (!hasItems && !hasServices) {
            event.preventDefault();
            alert("You must add at least one product or one service to the invoice.");
            return false;
        }
    });
});