// Static/js/global.js
document.addEventListener('DOMContentLoaded', function() {
    // Existing redirect-after-login logic
    const messages = document.querySelectorAll('.alert-success');
    const dashboardUrl = document.getElementById('dashboard-url')?.dataset.url || '/';
    messages.forEach(message => {
        if (message.textContent.includes('successfully logged in')) {
            window.location.href = dashboardUrl;
        }
    });

    // New logic for dynamic greeting based on time
    const greetingElement = document.getElementById('greeting-text');
    if (greetingElement) {
        const currentHour = new Date().getHours();
        let greeting = '';
        if (currentHour < 12) {
            greeting = 'Good Morning';
        } else if (currentHour < 17) {
            greeting = 'Good Afternoon';
        } else {
            greeting = 'Good Evening';
        }
        greetingElement.textContent = greeting;
    }
});