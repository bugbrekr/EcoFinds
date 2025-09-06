// Eco Wellness Login Form JavaScript
class EcoWellnessLoginForm {
    constructor() {
        this.form = document.getElementById('loginForm');
        this.emailInput = document.getElementById('email');
        this.submitButton = this.form.querySelector('.harmony-button');

        this.init();
    }

    init() {
        this.bindEvents();
    }

    bindEvents() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        this.emailInput.addEventListener('blur', () => this.validateEmail());
        this.emailInput.addEventListener('input', () => this.clearError('email'));

        // Add placeholder for label animations
        this.emailInput.setAttribute('placeholder', ' ');
    }

    validateEmail() {
        const email = this.emailInput.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!email) {
            this.showError('email', 'Please enter your email address.');
            return false;
        }

        if (!emailRegex.test(email)) {
            this.showError('email', 'Please enter a valid email address (e.g. user@example.com).');
            return false;
        }

        this.clearError('email');
        return true;
    }

    showError(field, message) {
        const organicField = document.getElementById(field).closest('.organic-field');
        const errorElement = document.getElementById(`${field}Error`);

        organicField.classList.add('error');
        errorElement.textContent = message;
        errorElement.classList.add('show');
    }

    clearError(field) {
        const organicField = document.getElementById(field).closest('.organic-field');
        const errorElement = document.getElementById(`${field}Error`);

        organicField.classList.remove('error');
        errorElement.classList.remove('show');
        errorElement.textContent = '';
    }

    validatePassword() {
        const passwordInput = document.getElementById('password');
        const password = passwordInput ? passwordInput.value : '';
        if (!password) {
            this.showError('password', 'Please enter your password.');
            return false;
        }
        if (password.length < 6) {
            this.showError('password', 'Password must be at least 6 characters long.');
            return false;
        }
        // Simulate incorrect password for demonstration
        if (password !== 'correctpassword') {
            this.showError('password', 'Incorrect password');
            return false;
        }
        this.clearError('password');
        return true;
    }

    async handleSubmit(e) {
        e.preventDefault();

        const isPasswordValid = this.validatePassword();
        if (!isPasswordValid) {
            return;
        }
        // Add delay animation to button
        this.submitButton.classList.add('loading');
        this.submitButton.disabled = true;
        setTimeout(() => {
            window.location.href = '/home/index.html';
        }, 1800); // 1.8 seconds delay
    }
}

// Initialize the wellness form when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new EcoWellnessLoginForm();
});