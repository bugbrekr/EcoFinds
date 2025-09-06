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

    async handleSubmit(e) {
        e.preventDefault();

        const isEmailValid = this.validateEmail();

        if (!isEmailValid) {
            return;
        }

        alert('Email submitted successfully!');
    }
}

// Initialize the wellness form when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new EcoWellnessLoginForm();
});