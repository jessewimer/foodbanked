// Location Detail Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Location detail page loaded');
    
    // Get location data from template
    const dataElement = document.getElementById('location-data');
    const locationData = JSON.parse(dataElement.textContent);
    
    // Initialize map if coordinates are available
    if (locationData.latitude && locationData.longitude) {
        initializeDetailMap(locationData);
    }
});

/**
 * Initialize detail map
 */
function initializeDetailMap(locationData) {
    const map = L.map('detailMap').setView(
        [locationData.latitude, locationData.longitude], 
        13
    );
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18,
    }).addTo(map);
    
    // Determine icon based on type
    const isFoodbank = locationData.type === 'foodbank';
    const iconColor = isFoodbank ? '#d97706' : '#0284c7';
    const iconClass = isFoodbank ? 'fa-store' : 'fa-building';
    
    // Create custom icon
    const locationIcon = L.divIcon({
        html: `<i class="fas ${iconClass}" style="color: ${iconColor}; font-size: 32px;"></i>`,
        className: 'custom-marker',
        iconSize: [40, 40],
        iconAnchor: [20, 20]
    });
    
    // Add marker
    const marker = L.marker(
        [locationData.latitude, locationData.longitude], 
        { icon: locationIcon }
    ).addTo(map);
    
    // Add popup with location name
    marker.bindPopup(`<strong>${escapeHtml(locationData.name)}</strong>`).openPopup();
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Export for potential use elsewhere
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeDetailMap,
        escapeHtml
    };
}