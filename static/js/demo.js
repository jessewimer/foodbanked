// Demo Visit Form JavaScript with Autocomplete Search
(function() {
    'use strict';
    
    // Parse patron data from script tag
    const patronDataElement = document.getElementById('patronData');
    const patrons = patronDataElement ? JSON.parse(patronDataElement.textContent) : [];
    
    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('demoVisitForm');
        const patronSearchSection = document.getElementById('patronSearchSection');
        const patronSearch = document.getElementById('patronSearch');
        const patronResults = document.getElementById('patronResults');
        const selectedPatronId = document.getElementById('selectedPatronId');
        const zipcodeInput = document.getElementById('zipcode');
        const successMessage = document.getElementById('successMessage');
        const resetButton = document.getElementById('resetForm');
        
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
            if (!patronSearchSection.contains(e.target)) {
                patronResults.classList.remove('show');
                selectedIndex = -1;
            }
        });
        
        // Handle form submission
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Validate age groups sum to household size
            const householdSize = parseInt(document.getElementById('householdSize').value);
            const age0_17 = parseInt(document.getElementById('age0_17').value) || 0;
            const age18_30 = parseInt(document.getElementById('age18_30').value) || 0;
            const age31_50 = parseInt(document.getElementById('age31_50').value) || 0;
            const age51_plus = parseInt(document.getElementById('age51_plus').value) || 0;
            const totalAges = age0_17 + age18_30 + age31_50 + age51_plus;
            
            if (totalAges !== householdSize) {
                alert(`Age groups must add up to household size (${householdSize}). Currently adds to ${totalAges}.`);
                return;
            }
            
            // Show success message
            successMessage.style.display = 'block';
            
            // Scroll to success message
            successMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            
            // Hide success message after 3 seconds and reset form
            setTimeout(function() {
                successMessage.style.display = 'none';
                form.reset();
                selectedPatronId.value = '';
                // Re-check the returning patron radio
                document.getElementById('returningPatron').checked = true;
                patronSearchSection.style.display = 'block';
            }, 3000);
        });
        
        // Handle reset button
        resetButton.addEventListener('click', function() {
            form.reset();
            selectedPatronId.value = '';
            successMessage.style.display = 'none';
            patronResults.classList.remove('show');
            document.getElementById('returningPatron').checked = true;
            patronSearchSection.style.display = 'block';
        });
        
        // Auto-update household size based on age groups
        const ageInputs = [
            document.getElementById('age0_17'),
            document.getElementById('age18_30'),
            document.getElementById('age31_50'),
            document.getElementById('age51_plus')
        ];
        
        ageInputs.forEach(input => {
            input.addEventListener('input', function() {
                const total = ageInputs.reduce((sum, inp) => {
                    return sum + (parseInt(inp.value) || 0);
                }, 0);
                
                if (total > 0) {
                    document.getElementById('householdSize').value = total;
                }
            });
        });
        
        // Handle "add new patron" link
        const addNewPatronLink = document.getElementById('addNewPatron');
        if (addNewPatronLink) {
            addNewPatronLink.addEventListener('click', function(e) {
                e.preventDefault();
                alert('In the real app, this would open a form to add a new patron to your database!');
            });
        }
    });
})();