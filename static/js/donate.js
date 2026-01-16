// Donate Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Donate page loaded');
    
    // Initialize amount button handlers
    setupAmountButtons();
    
    // Initialize custom amount handlers
    setupCustomAmountInputs();
    
    // Animate sections on scroll
    setupScrollAnimations();
});

/**
 * Setup amount button selection
 */
function setupAmountButtons() {
    const amountButtons = document.querySelectorAll('.amount-btn');
    
    amountButtons.forEach(button => {
        button.addEventListener('click', function() {
            const isMonthly = this.classList.contains('monthly');
            const section = this.closest('.donation-card');
            
            // Remove active class from all buttons in this section
            section.querySelectorAll('.amount-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Clear custom amount input
            const customInput = section.querySelector('input[type="number"]');
            if (customInput) {
                customInput.value = '';
            }
            
            // Store selected amount
            const amount = this.getAttribute('data-amount');
            console.log(`Selected amount: $${amount}${isMonthly ? '/month' : ''}`);
        });
    });
}

/**
 * Setup custom amount input handlers
 */
function setupCustomAmountInputs() {
    const customInputs = document.querySelectorAll('#customAmount, #customMonthly');
    
    customInputs.forEach(input => {
        input.addEventListener('input', function() {
            // Remove active class from all amount buttons in this section
            const section = this.closest('.donation-card');
            section.querySelectorAll('.amount-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Validate input (only positive numbers)
            if (this.value < 0) {
                this.value = 0;
            }
            
            // Remove decimal places for cleaner amounts
            if (this.value.includes('.')) {
                this.value = Math.floor(parseFloat(this.value));
            }
        });
        
        // Format on blur
        input.addEventListener('blur', function() {
            if (this.value && parseFloat(this.value) > 0) {
                this.value = Math.floor(parseFloat(this.value));
            }
        });
    });
}

/**
 * Setup scroll animations for sections
 */
function setupScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe sections
    const sections = document.querySelectorAll('.donation-card, .impact-item, .alternatives-section');
    sections.forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });
}

/**
 * Handle donation form submission
 * Note: This is a placeholder - you'll need to integrate with a payment processor
 */
function handleDonation(amount, isMonthly) {
    console.log(`Processing ${isMonthly ? 'monthly' : 'one-time'} donation of $${amount}`);
    
    // TODO: Integrate with payment processor (Stripe, PayPal, etc.)
    // For now, just show an alert
    alert(`Thank you for your interest in donating $${amount}${isMonthly ? '/month' : ''}! Payment processing will be integrated soon.`);
}

/**
 * Format currency
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
    }).format(amount);
}

// Export functions for potential use elsewhere
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        setupAmountButtons,
        setupCustomAmountInputs,
        setupScrollAnimations,
        handleDonation,
        formatCurrency
    };
}