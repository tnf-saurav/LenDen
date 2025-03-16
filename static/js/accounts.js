// document.addEventListener('DOMContentLoaded', function () {
//     const togglePassword = document.querySelector('.toggle-password');
//     const passwordInput = document.querySelector('#pass1');

//     togglePassword.addEventListener('click', function () {
//         const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
//         passwordInput.setAttribute('type', type);
//         this.classList.toggle('fa-eye');
//         this.classList.toggle('fa-eye-slash');
//     });
// });

document.addEventListener('DOMContentLoaded', function () {
    // Password toggle functionality
    const toggleIcons = document.querySelectorAll('.toggle-password');
    toggleIcons.forEach(icon => {
        const targetId = icon.getAttribute('data-target') || 'pass1';
        const passwordInput = document.querySelector(`#${targetId}`);

        icon.addEventListener('click', function () {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
        });
    });

    // Error handling functionality
    const inputs = document.querySelectorAll('input[data-error]');
    inputs.forEach(input => {
        const errorMessage = input.getAttribute('data-error');
        if (errorMessage) {
            // Clear the value and set the placeholder to the error message
            input.value = '';
            input.placeholder = errorMessage;
            input.classList.add('error-input');
        }

        // Clear the error when the user starts typing
        input.addEventListener('input', function () {
            if (this.classList.contains('error-input')) {
                this.classList.remove('error-input');
                this.placeholder = this.getAttribute('name').replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            }
        });
    });
});