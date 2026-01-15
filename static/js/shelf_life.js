// Shelf Life Search Functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('foodSearchInput');
    const searchResults = document.getElementById('searchResults');
    // const clearButton = document.getElementById('clearSearch');
    const modal = new bootstrap.Modal(document.getElementById('foodItemModal'));
    
    let searchTimeout;
    let currentFocus = -1;
    
    // Search input handler with debouncing
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        // Show/hide clear button
        // clearButton.style.display = query.length > 0 ? 'block' : 'none';
        
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
    // clearButton.addEventListener('click', function() {
    //     searchInput.value = '';
    //     clearButton.style.display = 'none';
    //     hideResults();
    //     searchInput.focus();
    // });
    
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
    
    // Show results again on focus if there's a query
    searchInput.addEventListener('focus', function() {
        if (this.value.trim().length >= 2 && searchResults.innerHTML) {
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
                    <i class="fas fa-search" style="font-size: 2.5rem;"></i>
                    <p>No items found matching "${escapeHtml(searchInput.value)}"</p>
                    <small>Try a different search term</small>
                </div>
            `;
            searchResults.style.display = 'block';
            return;
        }
        
        let html = '';
        
        // Add results count header
        html += `<div class="results-header">Found ${total} item${total !== 1 ? 's' : ''}</div>`;
        
        // Group results by category - clean headers, indented results
        for (const [category, items] of Object.entries(results)) {
            html += `
                <div class="category-group">
                    <div class="category-header">${category}</div>
            `;
            
            items.forEach(item => {
                html += `
                    <div class="result-item" data-item-id="${item.id}" tabindex="0">
                        <div class="result-name">${highlightMatch(item.name, searchInput.value)}</div>
                        <div class="result-details">
                            ${item.subcategory ? `<span class="subcategory">${escapeHtml(item.subcategory)}</span>` : ''}
                            <span class="shelf-life">
                                <i class="fas fa-clock me-1"></i>${escapeHtml(item.shelf_life)}
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
        if (!query) return escapeHtml(text);
        
        const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
        return escapeHtml(text).replace(regex, '<mark>$1</mark>');
    }
    
    // Escape HTML to prevent XSS
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
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
        document.getElementById('modalItemName').textContent = item.name;
        
        let content = `
            <div class="item-detail">
                <div class="detail-row">
                    <strong>Category</strong>
                    <span class="badge" style="background-color: ${getCategoryColor(item.category)}; color: white;">
                        ${escapeHtml(item.category_display)}
                    </span>
                </div>
        `;
        

        if (item.subcategory) {
            content += `
                <div class="detail-row">
                    <strong>Sub category</strong>
                    <span>${escapeHtml(item.subcategory)}</span>
                </div>
            `;
        }
        
        content += `
            <div class="detail-row">
                <strong>Shelf Life</strong>
                <span class="shelf-life-display">${escapeHtml(item.shelf_life_display)}</span>
            </div>
        `;
        
        if (item.has_numeric_shelf_life && item.shelf_life_max_days < 10000) {
            // Calculate the date by subtracting shelf life days from today
            const today = new Date();
            const okayToUseDate = new Date(today);
            okayToUseDate.setDate(today.getDate() - item.shelf_life_max_days);
            
            // Format date as "Month Day, Year"
            const formattedDate = okayToUseDate.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
            
            content += `
                <div class="detail-row">
                    <strong>Okay to use if date on package is after</strong>
                    <span>${formattedDate}</span>
                </div>
            `;
        }
        
        if (item.notes) {
            content += `
                <div class="detail-row mt-3">
                    <div class="alert mb-0">
                        <strong><i class="fas fa-info-circle me-2"></i>Storage Note</strong>
                        <p class="mb-0 mt-2">${escapeHtml(item.notes)}</p>
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
            'baby_food': '#d97706',
            'shelf_stable': '#059669',
            'refrigerated': '#0284c7',
            'frozen': '#4f46e5'
        };
        return colors[category] || '#6b7280';
    }
    
    // Hide search results
    function hideResults() {
        searchResults.style.display = 'none';
        currentFocus = -1;
    }
    
    // Show error message
    function showError(message) {
        searchResults.innerHTML = `
            <div class="alert alert-danger m-3">
                <i class="fas fa-exclamation-triangle me-2"></i>${escapeHtml(message)}
            </div>
        `;
        searchResults.style.display = 'block';
    }
});