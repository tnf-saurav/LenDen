// Modal Functionality
const addCustomerModal = document.getElementById("addCustomerModal");
const editCustomerModal = document.getElementById("editCustomerModal");
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

// Close Modals
closeButtons.forEach(button => {
    button.addEventListener("click", () => {
        addCustomerModal.style.display = "none";
        editCustomerModal.style.display = "none";
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
        // Check if this is the "No customers" row
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

    // If no rows are visible after filtering, show the "No customers" row
    if (!hasVisibleRows) {
        let emptyRow = Array.from(rows).find(row => 
            row.querySelector(".table-col")?.textContent.includes("No customers found")
        );
        if (emptyRow) {
            emptyRow.style.display = "flex";
        }
    }
}