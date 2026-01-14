// Shelf Life Search Functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('foodSearchInput');
    const searchResults = document.getElementById('searchResults');
    const clearButton = document.getElementById('clearSearch');
    const modal = new bootstrap.Modal(document.getElementById('foodItemModal'));
    
    let searchTimeout;
    let currentFocus = -1;
    
    // Category icons mapping
    const categoryIcons = {
        'Baby Food': '🍼',
        'Shelf-Stable': '🥫',
        'Refrigerated': '❄️',
        'Frozen': '🧊'
    };
    
    // Search input handler with debouncing
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        // Show/hide clear button
        clearButton.style.display = query.length > 0 ? 'block' : 'none';
        
        if (query.length < 2) {
            hideResults();
            return;
        }
        
        // Debounce search by 300ms
        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, 300);
    });
    
    // Clear search
    clearButton.addEventListener('click', function() {
        searchInput.value = '';
        clearButton.style.display = 'none';
        hideResults();
        searchInput.focus();
    });
    
    // Keyboard navigation
    searchInput.addEventListener('keydown', function(e) {
        const items = searchResults.querySelectorAll('.result-item');
        
        if (e.key === 'ArrowDown') {
            e.preventDefault();
            currentFocus++;
            setActive(items);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            currentFocus--;
            setActive(items);
        } else if (e.key === 'Enter') {
            e.preventDefault();
            if (currentFocus > -1 && items[currentFocus]) {
                items[currentFocus].click();
            }
        } else if (e.key === 'Escape') {
            hideResults();
        }
    });
    
    // Hide results when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            hideResults();
        }
    });
    
    // Focus on search input when clicking in the container
    searchInput.addEventListener('focus', function() {
        if (this.value.trim().length >= 2) {
            searchResults.style.display = 'block';
        }
    });
    
    // Perform search via API
    function performSearch(query) {
        fetch(`/resources/search/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                displayResults(data.results, data.total);
            })
            .catch(error => {
                console.error('Search error:', error);
                showError('Failed to search. Please try again.');
            });
    }
    
    // Display grouped search results
    function displayResults(results, total) {
        if (!results || Object.keys(results).length === 0) {
            searchResults.innerHTML = `
                <div class="no-results">
                    <i class="fas fa-search text-muted mb-2" style="font-size: 2rem;"></i>
                    <p class="mb-0">No items found matching "${searchInput.value}"</p>
                    <small class="text-muted">Try a different search term</small>
                </div>
            `;
            searchResults.style.display = 'block';
            return;
        }
        
        let html = '';
        
        // Add results count header
        html += `<div class="results-header">Found ${total} item${total !== 1 ? 's' : ''}</div>`;
        
        // Group results by category
        for (const [category, items] of Object.entries(results)) {
            html += `
                <div class="category-group">
                    <div class="category-header">
                        <span class="category-icon">${categoryIcons[category] || '📦'}</span>
                        <span class="category-name">${category}</span>
                        <span class="category-count">(${items.length})</span>
                    </div>
            `;
            
            items.forEach(item => {
                html += `
                    <div class="result-item" data-item-id="${item.id}" tabindex="0">
                        <div class="result-name">${highlightMatch(item.name, searchInput.value)}</div>
                        <div class="result-details">
                            ${item.subcategory ? `<span class="subcategory">${item.subcategory}</span>` : ''}
                            <span class="shelf-life">
                                <i class="fas fa-clock me-1"></i>${item.shelf_life}
                            </span>
                        </div>
                    </div>
                `;
            });
            
            html += '</div>';
        }
        
        searchResults.innerHTML = html;
        searchResults.style.display = 'block';
        currentFocus = -1;
        
        // Add click handlers to result items
        searchResults.querySelectorAll('.result-item').forEach(item => {
            item.addEventListener('click', function() {
                const itemId = this.getAttribute('data-item-id');
                showItemDetail(itemId);
            });
        });
    }
    
    // Highlight matching text in search results
    function highlightMatch(text, query) {
        if (!query) return text;
        
        const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }
    
    // Escape special regex characters
    function escapeRegex(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }
    
    // Set active item for keyboard navigation
    function setActive(items) {
        if (!items.length) return;
        
        // Remove active class from all items
        items.forEach(item => item.classList.remove('active'));
        
        // Wrap around
        if (currentFocus >= items.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = items.length - 1;
        
        // Add active class to current item
        items[currentFocus].classList.add('active');
        items[currentFocus].scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
    
    // Show item detail in modal
    function showItemDetail(itemId) {
        fetch(`/resources/item/${itemId}/`)
            .then(response => response.json())
            .then(data => {
                displayItemDetail(data);
                modal.show();
                hideResults();
            })
            .catch(error => {
                console.error('Error loading item:', error);
                showError('Failed to load item details. Please try again.');
            });
    }
    
    // Display item details in modal
    function displayItemDetail(item) {
        document.getElementById('modalItemName').innerHTML = `
            <span style="font-size: 1.5rem; margin-right: 8px;">${item.category_icon}</span>
            ${item.name}
        `;
        
        let content = `
            <div class="item-detail">
                <div class="detail-row">
                    <strong>Category:</strong>
                    <span class="badge" style="background-color: ${getCategoryColor(item.category)};">
                        ${item.category_display}
                    </span>
                </div>
        `;
        
        if (item.subcategory) {
            content += `
                <div class="detail-row">
                    <strong>Type:</strong>
                    <span>${item.subcategory}</span>
                </div>
            `;
        }
        
        content += `
            <div class="detail-row">
                <strong>Shelf Life:</strong>
                <span class="shelf-life-display">${item.shelf_life_display}</span>
            </div>
        `;
        
        if (item.has_numeric_shelf_life) {
            content += `
                <div class="detail-row">
                    <strong>Duration:</strong>
                    <span>${item.shelf_life_min_days}${item.shelf_life_min_days !== item.shelf_life_max_days ? ' - ' + item.shelf_life_max_days : ''} days</span>
                </div>
            `;
        }
        
        if (item.notes) {
            content += `
                <div class="detail-row mt-3">
                    <div class="alert alert-info mb-0">
                        <strong><i class="fas fa-info-circle me-2"></i>Note:</strong>
                        <p class="mb-0 mt-2">${item.notes}</p>
                    </div>
                </div>
            `;
        }
        
        content += '</div>';
        
        document.getElementById('modalContent').innerHTML = content;
    }
    
    // Get category color for badges
    function getCategoryColor(category) {
        const colors = {
            'baby_food': '#ff6b35',
            'shelf_stable': '#4a90e2',
            'refrigerated': '#2196f3',
            'frozen': '#1976d2'
        };
        return colors[category] || '#6c757d';
    }
    
    // Hide search results
    function hideResults() {
        searchResults.style.display = 'none';
        currentFocus = -1;
    }
    
    // Show error message
    function showError(message) {
        searchResults.innerHTML = `
            <div class="alert alert-danger mb-0">
                <i class="fas fa-exclamation-triangle me-2"></i>${message}
            </div>
        `;
        searchResults.style.display = 'block';
    }
});