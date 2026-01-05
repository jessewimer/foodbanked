// Demo Visit Form JavaScript - Matches actual visit form functionality
(function() {
    'use strict';
    
    // Parse patron data from script tag
    const patronDataElement = document.getElementById('patronData');
    const patrons = patronDataElement ? JSON.parse(patronDataElement.textContent) : [];
    
    console.log('Demo loaded with', patrons.length, 'patrons');
    
    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('demoVisitForm');
        const patronSearchSection = document.getElementById('patronSearchSection');
        const patronSearch = document.getElementById('patronSearch');
        const patronResults = document.getElementById('patronResults');
        const selectedPatronId = document.getElementById('selectedPatronId');
        const searchTypeSelect = document.getElementById('searchType');
        
        // Form fields
        const zipcodeInput = document.getElementById('zipcode');
        const householdSizeInput = document.getElementById('householdSize');
        const age0_18Input = document.getElementById('age0_18');
        const age19_59Input = document.getElementById('age19_59');
        const age60PlusInput = document.getElementById('age60_plus');
        
        // Sections
        const visitCountSection = document.getElementById('visitCountSection');
        const firstVisitSection = document.getElementById('firstVisitSection');
        const successMessage = document.getElementById('successMessage');
        const resetButton = document.getElementById('resetForm');
        
        // Handle visit type toggle
        const visitTypeRadios = document.querySelectorAll('input[name="visitType"]');
        
        visitTypeRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                if (this.value === 'anonymous') {
                    patronSearchSection.style.display = 'none';
                    visitCountSection.style.display = 'none';
                    firstVisitSection.style.display = 'block';
                    
                    patronSearch.value = '';
                    selectedPatronId.value = '';
                    patronResults.classList.remove('show');
                    clearFormFields();
                } else {
                    patronSearchSection.style.display = 'block';
                    firstVisitSection.style.display = 'none';
                    visitCountSection.style.display = 'none';
                }
            });
        });
        
        // Update search placeholder based on dropdown
        searchTypeSelect.addEventListener('change', function() {
            const searchType = this.value;
            if (searchType === 'last_name') {
                patronSearch.placeholder = 'Search by last name...';
            } else if (searchType === 'first_name') {
                patronSearch.placeholder = 'Search by first name...';
            } else if (searchType === 'address') {
                patronSearch.placeholder = 'Search by address...';
            }
            
            patronSearch.value = '';
            selectedPatronId.value = '';
            visitCountSection.style.display = 'none';
            patronResults.classList.remove('show');
            selectedIndex = -1;
        });
        
        // Autocomplete search with smart matching
        let selectedIndex = -1;
        
        patronSearch.addEventListener('input', function() {
            const searchTerm = this.value.trim();
            const searchType = searchTypeSelect.value;
            
            if (searchTerm.length === 0) {
                patronResults.classList.remove('show');
                selectedPatronId.value = '';
                visitCountSection.style.display = 'none';
                return;
            }
            
            const matches = filterPatrons(searchTerm, searchType);
            
            if (matches.length > 0) {
                displayResults(matches);
                selectedIndex = -1;
            } else {
                displayNoResults();
            }
        });
        
        // Smart filtering function
        function filterPatrons(searchTerm, searchType) {
            const lowerSearchTerm = searchTerm.toLowerCase();
            
            if (searchType === 'last_name') {
                if (lowerSearchTerm.startsWith('*')) {
                    const partialTerm = lowerSearchTerm.substring(1);
                    return patrons.filter(patron => 
                        patron.last_name.toLowerCase().includes(partialTerm)
                    );
                } else {
                    return patrons.filter(patron => 
                        patron.last_name.toLowerCase().startsWith(lowerSearchTerm)
                    );
                }
            } else if (searchType === 'first_name') {
                return patrons.filter(patron => 
                    patron.first_name.toLowerCase().includes(lowerSearchTerm)
                );
            } else if (searchType === 'address') {
                return patrons.filter(patron => 
                    patron.address && patron.address.toLowerCase().includes(lowerSearchTerm)
                );
            }
            
            return [];
        }
        
        // Display search results
        function displayResults(matches) {
            patronResults.innerHTML = '';
            
            matches.forEach((patron, index) => {
                const item = document.createElement('div');
                item.className = 'autocomplete-item';
                item.dataset.index = index;
                item.dataset.patronId = patron.id;
                
                item.innerHTML = `
                    <div class="autocomplete-item-name">${patron.last_name}, ${patron.first_name}</div>
                    <div class="autocomplete-item-details">${patron.address || 'No address'} • ${patron.zipcode}</div>
                `;
                
                item.addEventListener('click', function() {
                    selectPatron(patron);
                });
                
                patronResults.appendChild(item);
            });
            
            patronResults.classList.add('show');
        }
        
        // Display no results
        function displayNoResults() {
            patronResults.innerHTML = '<div class="autocomplete-no-results">No matching patrons found</div>';
            patronResults.classList.add('show');
        }
        
        // Select patron and auto-populate
        function selectPatron(patron) {
            patronSearch.value = `${patron.last_name}, ${patron.first_name}`;
            selectedPatronId.value = patron.id;
            patronResults.classList.remove('show');
            
            // Auto-populate from last visit
            if (patron.last_visit) {
                zipcodeInput.value = patron.last_visit.zipcode;
                householdSizeInput.value = patron.last_visit.household_size;
                age0_18Input.value = patron.last_visit.age_0_18;
                age19_59Input.value = patron.last_visit.age_19_59;
                age60PlusInput.value = patron.last_visit.age_60_plus;
            } else {
                zipcodeInput.value = patron.zipcode;
            }
            
            // Display visit count
            displayVisitCount(patron);
        }
        
        // Display visit count
        function displayVisitCount(patron) {
            if (patron.visits_this_month !== undefined && patron.last_visit_date) {
                const count = patron.visits_this_month;
                document.getElementById('visitCountNumber').textContent = count;
                document.getElementById('visitCountPlural').textContent = count === 1 ? '' : 's';
                document.getElementById('lastVisitDate').textContent = formatDate(patron.last_visit_date);
                visitCountSection.style.display = 'flex';
            } else {
                visitCountSection.style.display = 'none';
            }
        }
        
        // Format date
        function formatDate(dateString) {
            const date = new Date(dateString);
            const options = { month: 'short', day: 'numeric', year: 'numeric' };
            return date.toLocaleDateString('en-US', options);
        }
        
        // Clear form fields
        function clearFormFields() {
            zipcodeInput.value = '';
            householdSizeInput.value = '1';
            age0_18Input.value = '0';
            age19_59Input.value = '0';
            age60PlusInput.value = '0';
        }
        
        // Keyboard navigation
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
        
        // Update visual selection
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
        
        // Auto-update household size
        const ageInputs = [age0_18Input, age19_59Input, age60PlusInput];
        
        ageInputs.forEach(input => {
            input.addEventListener('input', function() {
                const total = ageInputs.reduce((sum, inp) => {
                    return sum + (parseInt(inp.value) || 0);
                }, 0);
                
                if (total > 0) {
                    householdSizeInput.value = total;
                }
            });
        });
        
        // Handle form submission
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Validate age groups sum to household size
            const householdSize = parseInt(householdSizeInput.value);
            const age0_18 = parseInt(age0_18Input.value) || 0;
            const age19_59 = parseInt(age19_59Input.value) || 0;
            const age60_plus = parseInt(age60PlusInput.value) || 0;
            const totalAges = age0_18 + age19_59 + age60_plus;
            
            if (totalAges !== householdSize) {
                alert(`Age groups must add up to household size (${householdSize}). Currently adds to ${totalAges}.`);
                return;
            }
            
            // Show success message
            successMessage.style.display = 'block';
            successMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            
            // Hide and reset after 3 seconds
            setTimeout(function() {
                successMessage.style.display = 'none';
                form.reset();
                selectedPatronId.value = '';
                document.getElementById('returningPatron').checked = true;
                patronSearchSection.style.display = 'block';
                visitCountSection.style.display = 'none';
                firstVisitSection.style.display = 'none';
            }, 3000);
        });
        
        // Handle reset button
        resetButton.addEventListener('click', function() {
            form.reset();
            selectedPatronId.value = '';
            successMessage.style.display = 'none';
            patronResults.classList.remove('show');
            visitCountSection.style.display = 'none';
            document.getElementById('returningPatron').checked = true;
            patronSearchSection.style.display = 'block';
            firstVisitSection.style.display = 'none';
        });
    });
})();