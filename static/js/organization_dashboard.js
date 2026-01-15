// Organization Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Organization Dashboard loaded');
    
    // Add smooth animations to stat cards
    animateStatCards();
    
    // Add loading states for quick action cards
    setupQuickActions();
});

/**
 * Animate stat cards on page load
 */
function animateStatCards() {
    const statCards = document.querySelectorAll('.stat-card');
    
    statCards.forEach((card, index) => {
        // Add slight delay for each card
        setTimeout(() => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            
            // Fade in animation
            setTimeout(() => {
                card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 50);
        }, index * 100);
    });
}

/**
 * Setup quick action card interactions
 */
function setupQuickActions() {
    const quickActionCards = document.querySelectorAll('.quick-action-card');
    
    quickActionCards.forEach(card => {
        // Add ripple effect on click
        card.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

/**
 * Format large numbers with commas
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/**
 * Animate number counting up
 */
function animateValue(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16); // 60fps
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            element.textContent = formatNumber(end);
            clearInterval(timer);
        } else {
            element.textContent = formatNumber(Math.floor(current));
        }
    }, 16);
}

// Export functions for potential use elsewhere
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        animateStatCards,
        setupQuickActions,
        formatNumber,
        animateValue
    };
}