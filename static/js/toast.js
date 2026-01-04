// Toast Notification System
(function() {
    'use strict';
    
    // Create toast container if it doesn't exist
    function getToastContainer() {
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        return container;
    }
    
    // Show toast notification
    function showToast(message, type = 'success', duration = 3000) {
        const container = getToastContainer();
        
        const toast = document.createElement('div');
        toast.className = `toast-notification toast-${type}`;
        
        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ'
        };
        
        toast.innerHTML = `
            <div class="toast-icon">${icons[type] || icons.success}</div>
            <div class="toast-content">
                <p class="toast-message">${message}</p>
            </div>
            <button class="toast-close" aria-label="Close">&times;</button>
        `;
        
        container.appendChild(toast);
        
        // Close button functionality
        const closeBtn = toast.querySelector('.toast-close');
        closeBtn.addEventListener('click', () => {
            removeToast(toast);
        });
        
        // Auto-dismiss after duration
        setTimeout(() => {
            removeToast(toast);
        }, duration);
    }
    
    // Remove toast with animation
    function removeToast(toast) {
        toast.classList.add('toast-fade-out');
        setTimeout(() => {
            toast.remove();
        }, 300);
    }
    
    // Make showToast globally available
    window.showToast = showToast;
    
    // Auto-show Django messages as toasts
    document.addEventListener('DOMContentLoaded', function() {
        const djangoMessages = document.querySelectorAll('.django-message');
        djangoMessages.forEach(msg => {
            const message = msg.textContent.trim();
            const type = msg.dataset.type || 'success';
            showToast(message, type);
        });
    });
})();