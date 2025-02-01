document.addEventListener('DOMContentLoaded', function() {
    const errorPopup = document.getElementById('error-popup');
    const closeButton = errorPopup.querySelector('.close');

    // Check if the error popup should be shown
    if (typeof showErrorPopup !== 'undefined' && showErrorPopup) {
        errorPopup.style.display = 'block';
    }

    // Close the error popup
    closeButton.addEventListener('click', function() {
        errorPopup.style.display = 'none';
    });
});



document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signup-form');
    const errorPopup = document.getElementById('error-popup');
    const errorList = document.getElementById('error-list');

    // Function to display errors
    const displayErrors = () => {
        // Ensure error list is empty before displaying new errors
        errorList.innerHTML = '';
        
        // Check for errors from the form and add them to the list
        const errors = [
            'businessname: User register with this Businessname already exists.',
            'phone: User register with this Phone already exists.',
            'email: User register with this Email already exists.'
        ];

        // Add each error as a list item
        errors.forEach((error) => {
            const li = document.createElement('li');
            li.textContent = error;
            errorList.appendChild(li);
        });

        // Show the error popup if there are any errors
        if (errors.length > 0) {
            errorPopup.style.display = 'block'; // Show the pop-up
            errorPopup.classList.add('show'); // Trigger animation
        }
    };

    // Show errors on page load (if any)
    displayErrors();

    // Close the pop-up when the close button is clicked
    const closeButton = errorPopup.querySelector('.close');
    closeButton.addEventListener('click', function() {
        errorPopup.classList.remove('show');
        errorPopup.style.display = 'none'; // Hide the pop-up when close button is clicked
    });

    form.addEventListener('submit', function(event) {
        // Simulating form errors for demonstration, you can replace this logic
        const errors = [
            'businessname: User register with this Businessname already exists.',
            'phone: User register with this Phone already exists.',
            'email: User register with this Email already exists.'
        ];

        // Prevent form submission if there are errors
        if (errors.length > 0) {
            event.preventDefault();
            errorPopup.style.display = 'block'; // Show the pop-up
            errorPopup.classList.add('show'); // Trigger slide-down animation
        } else {
            errorPopup.classList.remove('show'); // Hide the pop-up if no errors
        }
    });
});


// Toggle password visibility
const togglePassword1 = document.getElementById('toggle-password1');
const password1 = document.getElementById('password1');
togglePassword1.addEventListener('click', function() {
    const type = password1.getAttribute('type') === 'password' ? 'text' : 'password';
    password1.setAttribute('type', type);
    this.classList.toggle('fa-eye-slash');
});

const togglePassword2 = document.getElementById('toggle-password2');
const password2 = document.getElementById('password2');
togglePassword2.addEventListener('click', function() {
    const type = password2.getAttribute('type') === 'password' ? 'text' : 'password';
    password2.setAttribute('type', type);
    this.classList.toggle('fa-eye-slash');
});
