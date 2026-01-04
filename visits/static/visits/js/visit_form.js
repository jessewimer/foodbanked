// Visit Form JavaScript with Autocomplete Search
(function() {
    'use strict';
    
    // Parse patron data from script tag
    const patronDataElement = document.getElementById('patronData');
    const patrons = patronDataElement ? JSON.parse(patronDataElement.textContent) : [];
    
    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('visitForm');
        const patronSearchSection = document.getElementById('patronSearchSection');
        const patronSearch = document.getElementById('patronSearch');
        const patronResults = document.getElementById('patronResults');
        const selectedPatronId = document.getElementById('selectedPatronId');
        const zipcodeInput = document.getElementById('id_zipcode');
        
        // Handle visit type toggle
        const visitTypeRadios = document.querySelectorAll('input[name="visitType"]');
        visitTypeRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.value === 'anonymous') {
                    patronSearchSection.style.display = 'none';
                    patronSearch.value = '';
                    selectedPatronId.value = '';
                    zipcodeInput.value = '';
                    patronResults.classList.remove('show');
                } else {
                    patronSearchSection.style.display = 'block';
                }
            });
        });
        
        // Autocomplete search functionality
        let selectedIndex = -1;
        
        patronSearch.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase().trim();
            
            if (searchTerm.length === 0) {
                patronResults.classList.remove('show');
                selectedPatronId.value = '';
                return;
            }
            
            // Filter patrons by name or address
            const matches = patrons.filter(patron => {
                return patron.name.toLowerCase().includes(searchTerm) || 
                       patron.address.toLowerCase().includes(searchTerm);
            });
            
            if (matches.length > 0) {
                displayResults(matches);
                selectedIndex = -1;
            } else {
                displayNoResults();
            }
        });
        
        // Display search results
        function displayResults(matches) {
            patronResults.innerHTML = '';
            
            matches.forEach((patron, index) => {
                const item = document.createElement('div');
                item.className = 'autocomplete-item';
                item.dataset.index = index;
                item.dataset.patronId = patron.id;
                item.dataset.zipcode = patron.zipcode;
                
                item.innerHTML = `
                    <div class="autocomplete-item-name">${patron.name}</div>
                    <div class="autocomplete-item-details">${patron.address} • ${patron.zipcode}</div>
                `;
                
                item.addEventListener('click', function() {
                    selectPatron(patron);
                });
                
                patronResults.appendChild(item);
            });
            
            patronResults.classList.add('show');
        }
        
        // Display no results message
        function displayNoResults() {
            patronResults.innerHTML = '<div class="autocomplete-no-results">No matching patrons found</div>';
            patronResults.classList.add('show');
        }
        
        // Select a patron from results
        function selectPatron(patron) {
            patronSearch.value = patron.name;
            selectedPatronId.value = patron.id;
            zipcodeInput.value = patron.zipcode;
            patronResults.classList.remove('show');
        }
        
        // Keyboard navigation for autocomplete
        patronSearch.addEventListener('keydown', function(e) {
            const items = patronResults.querySelectorAll('.autocomplete-item');
            
            if (items.length === 0) return;
            
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                selectedIndex = (selectedIndex + 1) % items.length;
                updateSelection(items);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                selectedIndex = selectedIndex <= 0 ? items.length - 1 : selectedIndex - 1;
                updateSelection(items);
            } else if (e.key === 'Enter' && selectedIndex >= 0) {
                e.preventDefault();
                const selectedItem = items[selectedIndex];
                const patronId = selectedItem.dataset.patronId;
                const patron = patrons.find(p => p.id == patronId);
                if (patron) {
                    selectPatron(patron);
                }
            } else if (e.key === 'Escape') {
                patronResults.classList.remove('show');
                selectedIndex = -1;
            }
        });
        
        // Update visual selection in results
        function updateSelection(items) {
            items.forEach((item, index) => {
                if (index === selectedIndex) {
                    item.classList.add('selected');
                    item.scrollIntoView({ block: 'nearest' });
                } else {
                    item.classList.remove('selected');
                }
            });
        }
        
        // Close results when clicking outside
        document.addEventListener('click', function(e) {
            if (patronSearchSection && !patronSearchSection.contains(e.target)) {
                patronResults.classList.remove('show');
                selectedIndex = -1;
            }
        });
        
        // Auto-update household size based on age groups
        const ageInputs = [
            document.getElementById('id_age_0_17'),
            document.getElementById('id_age_18_30'),
            document.getElementById('id_age_31_50'),
            document.getElementById('id_age_51_plus')
        ];
        
        ageInputs.forEach(input => {
            if (input) {
                input.addEventListener('input', function() {
                    const total = ageInputs.reduce((sum, inp) => {
                        return sum + (parseInt(inp.value) || 0);
                    }, 0);
                    
                    if (total > 0) {
                        document.getElementById('id_household_size').value = total;
                    }
                });
            }
        });
    });
})();