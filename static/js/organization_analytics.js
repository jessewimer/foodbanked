// Organization Analytics JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Organization Analytics loaded');
    
    // Animate stat cards on page load
    animateStatCards();
    
    // Animate feature items
    animateFeatureItems();
    
    // Add number formatting to stat values
    formatStatNumbers();
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
 * Animate feature items
 */
function animateFeatureItems() {
    const featureItems = document.querySelectorAll('.feature-item');
    
    featureItems.forEach((item, index) => {
        setTimeout(() => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(15px)';
            
            setTimeout(() => {
                item.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
                item.style.opacity = '1';
                item.style.transform = 'translateY(0)';
            }, 50);
        }, 500 + (index * 100));
    });
}

/**
 * Format numbers with commas
 */
function formatStatNumbers() {
    const statValues = document.querySelectorAll('.stat-value');
    
    statValues.forEach(stat => {
        const value = parseInt(stat.textContent);
        if (!isNaN(value)) {
            stat.textContent = formatNumber(value);
        }
    });
    
    // Also format table stat badges
    const statBadges = document.querySelectorAll('.stat-badge');
    statBadges.forEach(badge => {
        const value = parseInt(badge.textContent);
        if (!isNaN(value)) {
            badge.textContent = formatNumber(value);
        }
    });
}

/**
 * Format large numbers with commas
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/**
 * Animate value counting up (for future use)
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
        animateFeatureItems,
        formatStatNumbers,
        formatNumber,
        animateValue
    };
}