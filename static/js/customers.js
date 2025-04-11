// Modal Functionality
const addCustomerModal = document.getElementById("addCustomerModal");
const editCustomerModal = document.getElementById("editCustomerModal");
const createInvoiceModal = document.getElementById("createInvoiceModal");
const addCustomerBtn = document.querySelector(".add-customer-btn");
const closeButtons = document.querySelectorAll(".close-btn");

function showAddCustomerModal() {
    addCustomerModal.style.display = "block";
}

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

closeButtons.forEach(button => {
    button.addEventListener("click", () => {
        addCustomerModal.style.display = "none";
        editCustomerModal.style.display = "none";
        createInvoiceModal.style.display = "none";
    });
});

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

function confirmDelete() {
    return confirm("Are you sure you want to delete this customer?");
}

// Search Functionality for Customer List Page
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

// Search Functionality for Customer Detail Page (Invoices)
const searchInvoices = () => {
    const input = getElement("#invoiceSearch")?.value.toLowerCase() || "";
    const rows = getElements(".table-body .table-row");
    let hasVisibleRows = false;

    rows.forEach(row => {
        const isEmptyRow = row.querySelector(".table-col")?.textContent.includes("No invoices found");
        if (isEmptyRow) {
            row.style.display = "none";
            return;
        }

        const date = row.querySelector(".table-col:nth-child(1)")?.textContent.toLowerCase() || "";
        const invoiceNumber = row.querySelector(".table-col:nth-child(2)")?.textContent.toLowerCase() || "";
        const billAmount = row.querySelector(".table-col:nth-child(3)")?.textContent.toLowerCase() || "";

        if (date.includes(input) || invoiceNumber.includes(input) || billAmount.includes(input)) {
            row.style.display = "flex";
            hasVisibleRows = true;
        } else {
            row.style.display = "none";
        }
    });

    if (!hasVisibleRows) {
        const emptyRow = Array.from(rows).find(row =>
            row.querySelector(".table-col")?.textContent.includes("No invoices found")
        );
        if (emptyRow) {
            emptyRow.style.display = "flex";
        }
    }
};

// Auto-submit search form on Enter key for Customer Detail Page
document.addEventListener("DOMContentLoaded", function() {
    const invoiceSearchInput = document.getElementById("invoiceSearch");
    if (invoiceSearchInput) {
        invoiceSearchInput.addEventListener("keypress", function(event) {
            if (event.key === "Enter") {
                event.preventDefault();
                invoiceSearchInput.closest("form").submit();
            }
        });
    }
});

// Invoice Functionality
$(document).ready(function() {
    let emptyItemRow = null;
    let emptyServiceRow = null;

    function initializeAutocomplete() {
        $('.product-autocomplete').each(function() {
            $(this).autocomplete({
                source: productAutocompleteUrl,
                minLength: 1,
                select: function(event, ui) {
                    $(this).siblings('input[type="hidden"]').val(ui.item.id);
                    console.log('Selected product ID:', ui.item.id);
                    console.log('Hidden input value:', $(this).siblings('input[type="hidden"]').val());
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

    if ($('#item-formset tr.item-row').length > 0) {
        emptyItemRow = $('#item-formset tr.item-row:first').clone(true);
    }
    if ($('#service-formset tr.service-row').length > 0) {
        emptyServiceRow = $('#service-formset tr.service-row:first').clone(true);
    }
    initializeAutocomplete();

    $('#add-item').on('click', function(e) {
        e.preventDefault();
        console.log('Add Product button clicked');
        let formIdx = parseInt($('#id_items-TOTAL_FORMS').val());
        console.log('Current item form index:', formIdx);
        console.log('Existing item rows:', $('#item-formset tr.item-row').length);

        let newRow;
        if (emptyItemRow && $('#item-formset tr.item-row').length > 0) {
            console.log('Cloning existing item row');
            newRow = emptyItemRow.clone(true);
        } else {
            console.log('Creating new item row from scratch');
            newRow = $('<tr class="item-row">' +
                '<td><div class="form-group">' +
                    '<input type="text" name="items-' + formIdx + '-product_name" class="product-autocomplete form-control" placeholder="Search for a product...">' +
                    '<input type="hidden" name="items-' + formIdx + '-product">' +
                    '<input type="hidden" name="items-' + formIdx + '-id">' +
                '</div></td>' +
                '<td><div class="form-group"><input type="number" name="items-' + formIdx + '-quantity" min="1" class="form-control"></div></td>' +
                '<td><div class="form-group"><input type="number" name="items-' + formIdx + '-unit_price" step="0.01" class="form-control"></div></td>' +
                '<td><div class="form-group"><input type="text" class="total-price form-control" value="0.00" readonly></div></td>' +
                '<td><button type="button" class="remove-item"><i class="fas fa-trash-alt"></i> Remove</button></td>' +
                '</tr>');
        }

        newRow.find('input').each(function() {
            let name = $(this).attr('name');
            if (name) {
                $(this).attr('name', name.replace(/-\d+-/, '-' + formIdx + '-'));
            }
            let id = $(this).attr('id');
            if (id) {
                $(this).attr('id', id.replace(/-\d+-/, '-' + formIdx + '-'));
            }
            let nameStr = $(this).attr('name') || '';
            if ($(this).hasClass('product-autocomplete') || nameStr.includes('product') || nameStr.includes('id')) {
                $(this).val('');
            } else {
                $(this).val($(this).hasClass('total-price') ? '0.00' : '');
            }
        });

        $('#item-formset').append(newRow);
        $('#id_items-TOTAL_FORMS').val(formIdx + 1);
        initializeAutocomplete();
        calculateTotal();
    });

    $('#add-service').on('click', function(e) {
        e.preventDefault();
        console.log('Add Service button clicked');
        let formIdx = parseInt($('#id_services-TOTAL_FORMS').val());
        console.log('Current service form index:', formIdx);

        let newRow;
        if (emptyServiceRow && $('#service-formset tr.service-row').length > 0) {
            console.log('Cloning existing service row');
            newRow = emptyServiceRow.clone(true);
        } else {
            console.log('Creating new service row from scratch');
            newRow = $('<tr class="service-row">' +
                '<td><div class="form-group"><input type="text" name="services-' + formIdx + '-description" class="form-control"></div></td>' +
                '<td><div class="form-group"><input type="number" name="services-' + formIdx + '-price" step="0.01" class="form-control"></div></td>' +
                '<td><button type="button" class="remove-service"><i class="fas fa-trash-alt"></i> Remove</button></td>' +
                '</tr>');
        }

        newRow.find('input').each(function() {
            let name = $(this).attr('name');
            if (name) {
                $(this).attr('name', name.replace(/-\d+-/, '-' + formIdx + '-'));
            }
            let id = $(this).attr('id');
            if (id) {
                $(this).attr('id', id.replace(/-\d+-/, '-' + formIdx + '-'));
            }
            $(this).val('');
        });

        $('#service-formset').append(newRow);
        $('#id_services-TOTAL_FORMS').val(formIdx + 1);
        calculateTotal();
    });

    $(document).on('click', '.remove-item', function() {
        if ($('.item-row').length > 1) {
            $(this).closest('.item-row').remove();
            calculateTotal();
        } else {
            $(this).closest('.item-row').remove();
            calculateTotal();
        }
    });

    $(document).on('click', '.remove-service', function() {
        if ($('.service-row').length > 1) {
            $(this).closest('.service-row').remove();
            calculateTotal();
        } else {
            $(this).closest('.service-row').remove();
            calculateTotal();
        }
    });

    $(document).on('input', 'input[name$="quantity"], input[name$="unit_price"], input[name$="price"], #id_discount_percent, #id_discount_amount', calculateTotal);

    function calculateTotal() {
        let total = 0;

        $('.item-row').each(function() {
            let qty = parseFloat($(this).find('input[name$="quantity"]').val()) || 0;
            let price = parseFloat($(this).find('input[name$="unit_price"]').val()) || 0;
            let itemTotal = qty * price;
            $(this).find('.total-price').val(itemTotal.toFixed(2));
            total += itemTotal;
        });

        $('.service-row').each(function() {
            let price = parseFloat($(this).find('input[name$="price"]').val()) || 0;
            total += price;
        });

        $('#total-amount').val(total.toFixed(2));
        let discountPercent = parseFloat($('#id_discount_percent').val()) || 0;
        let discountAmount = total * (discountPercent / 100);
        $('#id_discount_amount').val(discountAmount.toFixed(2));
        let finalAmount = total - discountAmount;
        $('#final-amount').val(finalAmount.toFixed(2));
    }

    $('#invoiceForm').on('submit', function(event) {
        let itemRows = $('.item-row');
        let serviceRows = $('.service-row');
        let hasItems = false;
        let hasServices = false;

        itemRows.each(function() {
            let productId = $(this).find('input[name$="product"]').val();
            let quantity = parseFloat($(this).find('input[name$="quantity"]').val()) || 0;
            if (productId && quantity > 0) {
                hasItems = true;
            }
        });

        serviceRows.each(function() {
            let price = parseFloat($(this).find('input[name$="price"]').val()) || 0;
            if (price > 0) {
                hasServices = true;
            }
        });

        if (!hasItems && !hasServices) {
            event.preventDefault();
            alert("You must add at least one product or one service to the invoice.");
            return false;
        }
    });

    calculateTotal();
});