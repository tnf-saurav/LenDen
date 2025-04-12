// // static/js/dashboard.js
// document.addEventListener('DOMContentLoaded', function () {
//     // Ensure Chart.js is loaded
//     if (typeof Chart === 'undefined') {
//         console.error('Chart.js is not loaded');
//         return;
//     }

//     // Sales Trend Chart (Daily)
//     const salesTrendCtx = document.getElementById('salesTrendChart');
//     const salesTrendFallback = document.getElementById('salesTrendChartFallback');
//     if (salesTrendCtx) {
//         const salesTrendDataSafe = Array.isArray(salesTrendData) && salesTrendData.length > 0 ? salesTrendData : [0];
//         const salesTrendLabels = salesTrendDataSafe.length > 0 ? Array.from({ length: salesTrendDataSafe.length }, (_, i) => i + 1) : ['No Data'];
//         if (salesTrendDataSafe.every(val => val === 0)) {
//             salesTrendCtx.style.display = 'none';
//             if (salesTrendFallback) salesTrendFallback.style.display = 'block';
//         } else {
//             new Chart(salesTrendCtx.getContext('2d'), {
//                 type: 'line',
//                 data: {
//                     labels: salesTrendLabels,
//                     datasets: [{
//                         label: 'Daily Sales (via Invoices)',
//                         data: salesTrendDataSafe,
//                         borderColor: 'rgba(75, 192, 192, 1)',
//                         backgroundColor: 'rgba(75, 192, 192, 0.2)',
//                         fill: true,
//                         tension: 0.3
//                     }]
//                 },
//                 options: {
//                     responsive: true,
//                     maintainAspectRatio: false,
//                     scales: {
//                         y: { beginAtZero: true, title: { display: true, text: 'Sales ($)' } },
//                         x: { title: { display: true, text: 'Day of Month' } }
//                     }
//                 }
//             });
//         }
//     } else {
//         console.error('Sales Trend Chart (Daily) canvas not found');
//     }

//     // Sales Trend Chart (Monthly)
//     const monthlySalesTrendCtx = document.getElementById('monthlySalesTrendChart');
//     const monthlySalesTrendFallback = document.getElementById('monthlySalesTrendChartFallback');
//     if (monthlySalesTrendCtx) {
//         const monthlySalesTrendDataSafe = Array.isArray(monthlySalesTrendData) && monthlySalesTrendData.length > 0 ? monthlySalesTrendData : [0];
//         const monthlySalesTrendLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
//         if (monthlySalesTrendDataSafe.every(val => val === 0)) {
//             monthlySalesTrendCtx.style.display = 'none';
//             if (monthlySalesTrendFallback) monthlySalesTrendFallback.style.display = 'block';
//         } else {
//             new Chart(monthlySalesTrendCtx.getContext('2d'), {
//                 type: 'line',
//                 data: {
//                     labels: monthlySalesTrendLabels,
//                     datasets: [{
//                         label: 'Monthly Sales (via Invoices)',
//                         data: monthlySalesTrendDataSafe,
//                         borderColor: 'rgba(153, 102, 255, 1)',
//                         backgroundColor: 'rgba(153, 102, 255, 0.2)',
//                         fill: true,
//                         tension: 0.3
//                     }]
//                 },
//                 options: {
//                     responsive: true,
//                     maintainAspectRatio: false,
//                     scales: {
//                         y: { beginAtZero: true, title: { display: true, text: 'Sales ($)' } },
//                         x: { title: { display: true, text: 'Month' } }
//                     }
//                 }
//             });
//         }
//     } else {
//         console.error('Sales Trend Chart (Monthly) canvas not found');
//     }

//     // Sales by Product Chart
//     const salesByProductCtx = document.getElementById('salesByProductChart');
//     const salesByProductFallback = document.getElementById('salesByProductChartFallback');
//     if (salesByProductCtx) {
//         const salesByProductDataSafe = Array.isArray(salesByProductData) && salesByProductData.length > 0 ? salesByProductData : [{ product_name: 'No Data', total: 0 }];
//         if (salesByProductDataSafe.length === 1 && salesByProductDataSafe[0].total === 0) {
//             salesByProductCtx.style.display = 'none';
//             if (salesByProductFallback) salesByProductFallback.style.display = 'block';
//         } else {
//             new Chart(salesByProductCtx.getContext('2d'), {
//                 type: 'bar',
//                 data: {
//                     labels: salesByProductDataSafe.map(item => item.product_name || 'No Data'),
//                     datasets: [{
//                         label: 'Sales ($)',
//                         data: salesByProductDataSafe.map(item => item.total || 0),
//                         backgroundColor: 'rgba(54, 162, 235, 0.5)',
//                         borderColor: 'rgba(54, 162, 235, 1)',
//                         borderWidth: 1
//                     }]
//                 },
//                 options: {
//                     responsive: true,
//                     maintainAspectRatio: false,
//                     scales: {
//                         y: { beginAtZero: true, title: { display: true, text: 'Sales ($)' } },
//                         x: { title: { display: true, text: 'Product' } }
//                     }
//                 }
//             });
//         }
//     } else {
//         console.error('Sales by Product Chart canvas not found');
//     }

//     // Inventory Status Chart
//     const inventoryStatusCtx = document.getElementById('inventoryStatusChart');
//     const inventoryStatusFallback = document.getElementById('inventoryStatusChartFallback');
//     if (inventoryStatusCtx) {
//         const inventoryStatusDataSafe = Array.isArray(inventoryStatusData) && inventoryStatusData.length > 0 ? inventoryStatusData : [{ product_name: 'No Data', stock_level: 0 }];
//         if (inventoryStatusDataSafe.length === 1 && inventoryStatusDataSafe[0].stock_level === 0) {
//             inventoryStatusCtx.style.display = 'none';
//             if (inventoryStatusFallback) inventoryStatusFallback.style.display = 'block';
//         } else {
//             new Chart(inventoryStatusCtx.getContext('2d'), {
//                 type: 'bar',
//                 data: {
//                     labels: inventoryStatusDataSafe.map(item => item.product_name || 'No Data'),
//                     datasets: [{
//                         label: 'Stock Level',
//                         data: inventoryStatusDataSafe.map(item => item.stock_level || 0),
//                         backgroundColor: 'rgba(255, 206, 86, 0.5)',
//                         borderColor: 'rgba(255, 206, 86, 1)',
//                         borderWidth: 1
//                     }]
//                 },
//                 options: {
//                     responsive: true,
//                     maintainAspectRatio: false,
//                     scales: {
//                         y: { beginAtZero: true, title: { display: true, text: 'Stock Level' } },
//                         x: { title: { display: true, text: 'Product' } }
//                     }
//                 }
//             });
//         }
//     } else {
//         console.error('Inventory Status Chart canvas not found');
//     }
// });

// static/js/dashboard.js
document.addEventListener('DOMContentLoaded', function () {
    // Ensure Chart.js is loaded
    if (typeof Chart === 'undefined') {
        console.error('Chart.js is not loaded');
        return;
    }

    // Sales Trend Chart (Daily)
    const salesTrendCtx = document.getElementById('salesTrendChart');
    const salesTrendFallback = document.getElementById('salesTrendChartFallback');
    if (salesTrendCtx) {
        const salesTrendDataSafe = Array.isArray(salesTrendData) && salesTrendData.length > 0 ? salesTrendData : [0];
        const salesTrendLabels = salesTrendDataSafe.length > 0 ? Array.from({ length: salesTrendDataSafe.length }, (_, i) => i + 1) : ['No Data'];
        if (salesTrendDataSafe.every(val => val === 0)) {
            salesTrendCtx.style.display = 'none';
            if (salesTrendFallback) salesTrendFallback.style.display = 'block';
        } else {
            new Chart(salesTrendCtx.getContext('2d'), {
                type: 'line',
                data: {
                    labels: salesTrendLabels,
                    datasets: [{
                        label: 'Daily Sales (via Invoices)',
                        data: salesTrendDataSafe,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        fill: true,
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true, title: { display: true, text: 'Sales ($)' } },
                        x: { title: { display: true, text: 'Day of Month' } }
                    }
                }
            });
        }
    } else {
        console.error('Sales Trend Chart (Daily) canvas not found');
    }

    // Sales Trend Chart (Monthly)
    const monthlySalesTrendCtx = document.getElementById('monthlySalesTrendChart');
    const monthlySalesTrendFallback = document.getElementById('monthlySalesTrendChartFallback');
    if (monthlySalesTrendCtx) {
        const monthlySalesTrendDataSafe = Array.isArray(monthlySalesTrendData) && monthlySalesTrendData.length > 0 ? monthlySalesTrendData : [0];
        const monthlySalesTrendLabels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        if (monthlySalesTrendDataSafe.every(val => val === 0)) {
            monthlySalesTrendCtx.style.display = 'none';
            if (monthlySalesTrendFallback) monthlySalesTrendFallback.style.display = 'block';
        } else {
            new Chart(monthlySalesTrendCtx.getContext('2d'), {
                type: 'line',
                data: {
                    labels: monthlySalesTrendLabels,
                    datasets: [{
                        label: 'Monthly Sales (via Invoices)',
                        data: monthlySalesTrendDataSafe,
                        borderColor: 'rgba(153, 102, 255, 1)',
                        backgroundColor: 'rgba(153, 102, 255, 0.2)',
                        fill: true,
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true, title: { display: true, text: 'Sales ($)' } },
                        x: { title: { display: true, text: 'Month' } }
                    }
                }
            });
        }
    } else {
        console.error('Sales Trend Chart (Monthly) canvas not found');
    }

    // Sales by Product Chart
    const salesByProductCtx = document.getElementById('salesByProductChart');
    const salesByProductFallback = document.getElementById('salesByProductChartFallback');
    if (salesByProductCtx) {
        const salesByProductDataSafe = Array.isArray(salesByProductData) && salesByProductData.length > 0 ? salesByProductData : [{ product_name: 'No Data', total: 0 }];
        if (salesByProductDataSafe.length === 1 && salesByProductDataSafe[0].total === 0) {
            salesByProductCtx.style.display = 'none';
            if (salesByProductFallback) salesByProductFallback.style.display = 'block';
        } else {
            new Chart(salesByProductCtx.getContext('2d'), {
                type: 'bar',
                data: {
                    labels: salesByProductDataSafe.map(item => item.product_name || 'No Data'),
                    datasets: [{
                        label: 'Sales ($)',
                        data: salesByProductDataSafe.map(item => item.total || 0),
                        backgroundColor: 'rgba(54, 162, 235, 0.5)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true, title: { display: true, text: 'Sales ($)' } },
                        x: { title: { display: true, text: 'Product' } }
                    }
                }
            });
        }
    } else {
        console.error('Sales by Product Chart canvas not found');
    }

    // Inventory Status Chart
    const inventoryStatusCtx = document.getElementById('inventoryStatusChart');
    const inventoryStatusFallback = document.getElementById('inventoryStatusChartFallback');
    if (inventoryStatusCtx) {
        const inventoryStatusDataSafe = Array.isArray(inventoryStatusData) && inventoryStatusData.length > 0 ? inventoryStatusData : [{ product_name: 'No Data', stock_level: 0 }];
        if (inventoryStatusDataSafe.length === 1 && inventoryStatusDataSafe[0].stock_level === 0) {
            inventoryStatusCtx.style.display = 'none';
            if (inventoryStatusFallback) inventoryStatusFallback.style.display = 'block';
        } else {
            new Chart(inventoryStatusCtx.getContext('2d'), {
                type: 'bar',
                data: {
                    labels: inventoryStatusDataSafe.map(item => item.product_name || 'No Data'),
                    datasets: [{
                        label: 'Stock Level',
                        data: inventoryStatusDataSafe.map(item => item.stock_level || 0),
                        backgroundColor: 'rgba(255, 206, 86, 0.5)',
                        borderColor: 'rgba(255, 206, 86, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true, title: { display: true, text: 'Stock Level' } },
                        x: { title: { display: true, text: 'Product' } }
                    }
                }
            });
        }
    } else {
        console.error('Inventory Status Chart canvas not found');
    }
});