// Locations Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Locations page loaded');
    
    // Get location data from template
    const dataElement = document.getElementById('locations-data');
    const data = JSON.parse(dataElement.textContent);
    
    // Initialize map
    initializeMap(data);
    
    // Initialize search
    initializeSearch();
});

/**
 * Initialize Leaflet map
 */
function initializeMap(data) {
    // Center on Idaho
    const map = L.map('map').setView([44.0682, -114.7420], 7);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18,
    }).addTo(map);
    
    // Custom icons
    const foodbankIcon = L.divIcon({
        html: '<i class="fas fa-store" style="color: #d97706; font-size: 24px;"></i>',
        className: 'custom-marker',
        iconSize: [30, 30],
        iconAnchor: [15, 15],
        popupAnchor: [0, -15]
    });
    
    const organizationIcon = L.divIcon({
        html: '<i class="fas fa-building" style="color: #0284c7; font-size: 24px;"></i>',
        className: 'custom-marker',
        iconSize: [30, 30],
        iconAnchor: [15, 15],
        popupAnchor: [0, -15]
    });
    
    // Add foodbank markers
    data.foodbanks.forEach(function(fb) {
        if (fb.latitude && fb.longitude) {
            const marker = L.marker([fb.latitude, fb.longitude], {
                icon: foodbankIcon
            }).addTo(map);
            
            marker.bindPopup(createPopupContent(fb, 'foodbank'));
        }
    });
    
    // Add organization markers
    data.organizations.forEach(function(org) {
        if (org.latitude && org.longitude) {
            const marker = L.marker([org.latitude, org.longitude], {
                icon: organizationIcon
            }).addTo(map);
            
            marker.bindPopup(createPopupContent(org, 'organization'));
        }
    });
    
    // Fit map to show all markers
    const allLocations = [];
    data.foodbanks.forEach(fb => {
        if (fb.latitude && fb.longitude) {
            allLocations.push([fb.latitude, fb.longitude]);
        }
    });
    data.organizations.forEach(org => {
        if (org.latitude && org.longitude) {
            allLocations.push([org.latitude, org.longitude]);
        }
    });
    
    if (allLocations.length > 0) {
        const bounds = L.latLngBounds(allLocations);
        map.fitBounds(bounds, { padding: [50, 50] });
    }
}

/**
 * Create popup content for markers
 */

function createPopupContent(location, type) {
    const cityState = location.city && location.state 
        ? `${location.city}, ${location.state}` 
        : 'Location not set';
    
    return `
        <div class="popup-content">
            <h3 class="popup-title">${escapeHtml(location.name)}</h3>
            <div class="popup-location">
                ${escapeHtml(cityState)}
            </div>
            <a href="/locations/${type}/${location.id}/" class="popup-button">
                View Details
            </a>
        </div>
    `;
}

/**
 * Initialize search functionality
 */
function initializeSearch() {
    const searchInput = document.getElementById('locationSearch');
    const searchResults = document.getElementById('searchResults');
    let searchTimeout;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        if (query.length < 2) {
            searchResults.style.display = 'none';
            return;
        }
        
        // Debounce search
        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, 300);
    });
    
    // Close search results when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.style.display = 'none';
        }
    });
    
    // Show results again on focus
    searchInput.addEventListener('focus', function() {
        if (this.value.trim().length >= 2 && searchResults.innerHTML) {
            searchResults.style.display = 'block';
        }
    });
}

/**
 * Perform search via AJAX
 */
function performSearch(query) {
    fetch(`/locations/search/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            displaySearchResults(data.results);
        })
        .catch(error => {
            console.error('Search error:', error);
        });
}

/**
 * Display search results
 */
function displaySearchResults(results) {
    const searchResults = document.getElementById('searchResults');
    
    if (results.length === 0) {
        searchResults.innerHTML = `
            <div class="no-results">
                <i class="fas fa-search" style="font-size: 2rem; opacity: 0.3;"></i>
                <p style="margin-top: 1rem;">No locations found</p>
            </div>
        `;
        searchResults.style.display = 'block';
        return;
    }
    
    let html = '';
    results.forEach(result => {
        const iconClass = result.type === 'foodbank' ? 'fa-store' : 'fa-building';
        html += `
            <a href="/locations/${result.type}/${result.id}/" class="search-result-item">
                <div class="result-icon ${result.type}">
                    <i class="fas ${iconClass}"></i>
                </div>
                <div class="result-info">
                    <div class="result-name">${escapeHtml(result.name)}</div>
                    <div class="result-location">${escapeHtml(result.location)}</div>
                </div>
            </a>
        `;
    });
    
    searchResults.innerHTML = html;
    searchResults.style.display = 'block';
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
        initializeMap,
        createPopupContent,
        initializeSearch,
        performSearch,
        displaySearchResults,
        escapeHtml
    };
}