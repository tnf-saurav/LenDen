// Search Functionality
function searchProducts() {
    let input = document.getElementById("inventorySearch").value.toLowerCase();
    let rows = document.querySelectorAll(".table-body .table-row");
    let hasVisibleRows = false;

    rows.forEach(row => {
        // Check if this is the "No products" row
        let isEmptyRow = row.querySelector(".table-col")?.textContent.includes("No products found");
        if (isEmptyRow) {
            row.style.display = "none";
            return;
        }

        let productName = row.querySelector(".table-col:nth-child(1)").textContent.toLowerCase();
        if (productName.includes(input)) {
            row.style.display = "flex";
            hasVisibleRows = true;
        } else {
            row.style.display = "none";
        }
    });

    // If no rows are visible after filtering, show the "No products" row
    if (!hasVisibleRows) {
        let emptyRow = Array.from(rows).find(row => 
            row.querySelector(".table-col")?.textContent.includes("No products found")
        );
        if (emptyRow) {
            emptyRow.style.display = "flex";
        }
    }
}