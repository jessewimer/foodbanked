// Organization Settings JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Organization Settings loaded');
    
    // Form validation and enhancement
    const form = document.getElementById('orgSettingsForm');
    
    if (form) {
        // Add Bootstrap form-control class to all form inputs
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.classList.add('form-control');
        });
        
        // Form submission handler
        form.addEventListener('submit', function(e) {
            // Add loading state to submit button
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Saving...';
            }
        });
        
        // Auto-format phone number as user types
        const phoneInput = document.getElementById('id_phone');
        if (phoneInput) {
            phoneInput.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                
                if (value.length > 0) {
                    if (value.length <= 3) {
                        e.target.value = value;
                    } else if (value.length <= 6) {
                        e.target.value = `(${value.slice(0, 3)}) ${value.slice(3)}`;
                    } else {
                        e.target.value = `(${value.slice(0, 3)}) ${value.slice(3, 6)}-${value.slice(6, 10)}`;
                    }
                }
            });
        }
        
        // State input to uppercase
        const stateInput = document.getElementById('id_state');
        if (stateInput) {
            stateInput.addEventListener('input', function(e) {
                e.target.value = e.target.value.toUpperCase();
                if (e.target.value.length > 2) {
                    e.target.value = e.target.value.slice(0, 2);
                }
            });
        }
        
        // Validate email format
        const emailInput = document.getElementById('id_email');
        if (emailInput) {
            emailInput.addEventListener('blur', function(e) {
                if (e.target.value && !isValidEmail(e.target.value)) {
                    showFieldError(e.target, 'Please enter a valid email address');
                } else {
                    clearFieldError(e.target);
                }
            });
        }
        
        // Validate website URL
        const websiteInput = document.getElementById('id_website');
        if (websiteInput) {
            websiteInput.addEventListener('blur', function(e) {
                if (e.target.value && !isValidURL(e.target.value)) {
                    showFieldError(e.target, 'Please enter a valid URL (e.g., https://example.org)');
                } else {
                    clearFieldError(e.target);
                }
            });
        }
    }
    
    // Add smooth animations to info groups
    animateInfoGroups();
});

/**
 * Validate email format
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Validate URL format
 */
function isValidURL(url) {
    try {
        new URL(url);
        return true;
    } catch {
        return false;
    }
}

/**
 * Show error message for a field
 */
function showFieldError(input, message) {
    clearFieldError(input);
    
    input.classList.add('is-invalid');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback d-block';
    errorDiv.textContent = message;
    input.parentNode.appendChild(errorDiv);
}

/**
 * Clear error message for a field
 */
function clearFieldError(input) {
    input.classList.remove('is-invalid');
    const errorDiv = input.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

/**
 * Animate info groups on page load
 */
function animateInfoGroups() {
    const infoGroups = document.querySelectorAll('.info-group');
    
    infoGroups.forEach((group, index) => {
        // Add slight delay for each group
        setTimeout(() => {
            group.style.opacity = '0';
            group.style.transform = 'translateY(10px)';
            
            // Fade in animation
            setTimeout(() => {
                group.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
                group.style.opacity = '1';
                group.style.transform = 'translateY(0)';
            }, 50);
        }, index * 50);
    });
}

// Export functions for potential use elsewhere
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        isValidEmail,
        isValidURL,
        showFieldError,
        clearFieldError,
        animateInfoGroups
    };
}