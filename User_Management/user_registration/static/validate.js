document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const emailInput = document.getElementById('email');
    const submitButton = document.querySelector('button[type="submit"]');

    // Function to validate username
    function validateUsername(username) {
        const usernamePattern = /^[a-zA-Z0-9_.]{3,20}$/;
        return usernamePattern.test(username);
    }

    // Function to validate email
    function validateEmail(email) {
        const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return emailPattern.test(email);
    }

    // Function to validate password
    function validatePassword(password) {
        const passwordPattern = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
        return passwordPattern.test(password);
    }

    // Function to validate the form
    function validateForm() {
        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();
        const email = emailInput.value.trim();
        let valid = true;

        // Validate username
        if (!validateUsername(username)) {
            showError(usernameInput, 'Invalid username. Must be 3-20 characters and can include alphanumeric characters, underscores, and periods.');
            valid = false;
        } else {
            clearError(usernameInput);
        }

        // Validate email
        if (!validateEmail(email)) {
            showError(emailInput, 'Invalid email address.');
            valid = false;
        } else {
            clearError(emailInput);
        }

        // Validate password
        if (!validatePassword(password)) {
            showError(passwordInput, 'Password must be at least 8 characters long, include at least one uppercase letter, one lowercase letter, one number, and one special character.');
            valid = false;
        } else {
            clearError(passwordInput);
        }

        return valid;
    }

    // Function to show error message
    function showError(input, message) {
        let error = input.nextElementSibling;
        if (!error || !error.classList.contains('error-message')) {
            error = document.createElement('div');
            error.classList.add('error-message');
            input.parentElement.appendChild(error);
        }
        error.textContent = message;
    }

    // Function to clear error message
    function clearError(input) {
        let error = input.nextElementSibling;
        if (error && error.classList.contains('error-message')) {
            error.remove();
        }
    }

    // Validate form on submit
    form.addEventListener('submit', (e) => {
        if (!validateForm()) {
            e.preventDefault(); // Prevent form submission if validation fails
        }
    });

    // Validate on input change
    [usernameInput, passwordInput, emailInput].forEach(input => {
        input.addEventListener('input', validateForm);
    });
});
