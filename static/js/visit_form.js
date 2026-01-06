// Visit Form JavaScript with Enhanced Search, Patron Info Display, and Inline Editing
(function() {
    'use strict';
    
    console.log('Visit form script loaded');
    
    // Parse patron data from script tag
    const patronDataElement = document.getElementById('patronData');
    let patrons = patronDataElement ? JSON.parse(patronDataElement.textContent) : [];
    
    console.log('Patrons loaded:', patrons.length);
    
    // Store currently selected patron for editing
    let currentPatron = null;
    
    document.addEventListener('DOMContentLoaded', function() {
        console.log('DOM loaded');
        
        const form = document.getElementById('visitForm');
        const patronSearchSection = document.getElementById('patronSearchSection');
        const patronSearch = document.getElementById('patronSearch');
        const patronResults = document.getElementById('patronResults');
        const selectedPatronId = document.getElementById('selectedPatronId');
        const searchTypeSelect = document.getElementById('searchType');
        
        // Patron info card elements
        const patronInfoCard = document.getElementById('patronInfoCard');
        const patronInfoName = document.getElementById('patronInfoName');
        const patronInfoAddress = document.getElementById('patronInfoAddress');
        const patronInfoCityState = document.getElementById('patronInfoCityState');
        const patronInfoZip = document.getElementById('patronInfoZip');
        const patronInfoComments = document.getElementById('patronInfoComments');
        const patronInfoCommentsRow = document.getElementById('patronInfoCommentsRow');
        const editPatronBtn = document.getElementById('editPatronBtn');
        
        // Modal elements
        const editPatronModal = new bootstrap.Modal(document.getElementById('editPatronModal'));
        const savePatronBtn = document.getElementById('savePatronBtn');
        
        console.log('Elements found:', {
            form: !!form,
            patronSearch: !!patronSearch,
            searchTypeSelect: !!searchTypeSelect,
            patronInfoCard: !!patronInfoCard
        });
        
        // Form fields
        const zipcodeInput = document.getElementById('id_zipcode');
        const householdSizeInput = document.getElementById('id_household_size');
        const age0_18Input = document.getElementById('id_age_0_18');
        const age19_59Input = document.getElementById('id_age_19_59');
        const age60PlusInput = document.getElementById('id_age_60_plus');
        
        // Visit count section
        const visitCountSection = document.getElementById('visitCountSection');
        const firstVisitSection = document.getElementById('firstVisitSection');
        
        // Handle visit type toggle
        const visitTypeRadios = document.querySelectorAll('input[name="visitType"]');
        
        // Check initial state on page load
        const initialChecked = document.querySelector('input[name="visitType"]:checked');
        console.log('Initial checked:', initialChecked ? initialChecked.value : 'none');
        
        if (initialChecked && initialChecked.value === 'anonymous') {
            console.log('Setting anonymous mode on load');
            patronSearchSection.style.display = 'none';
            patronInfoCard.style.display = 'none';
            visitCountSection.style.display = 'none';
            firstVisitSection.style.display = 'block';
        }
        
        visitTypeRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                console.log('Visit type changed to:', this.value);
                
                if (this.value === 'anonymous') {
                    // Show first visit checkbox, hide patron search, info card, and visit count
                    patronSearchSection.style.display = 'none';
                    patronInfoCard.style.display = 'none';
                    visitCountSection.style.display = 'none';
                    firstVisitSection.style.display = 'block';
                    
                    console.log('Anonymous mode: hiding patron search, showing first visit checkbox');
                    
                    // Clear patron selection and form
                    patronSearch.value = '';
                    selectedPatronId.value = '';
                    patronResults.classList.remove('show');
                    currentPatron = null;
                    clearFormFields();
                } else {
                    // Show patron search, hide first visit checkbox and info card
                    patronSearchSection.style.display = 'block';
                    firstVisitSection.style.display = 'none';
                    patronInfoCard.style.display = 'none';
                    visitCountSection.style.display = 'none';
                    
                    console.log('Returning mode: showing patron search, hiding first visit checkbox');
                }
            });
        });
        
        // Update search placeholder based on dropdown selection
        searchTypeSelect.addEventListener('change', function() {
            const searchType = this.value;
            console.log('Search type changed to:', searchType);
            
            if (searchType === 'last_name') {
                patronSearch.placeholder = 'Search by last name...';
            } else if (searchType === 'first_name') {
                patronSearch.placeholder = 'Search by first name...';
            } else if (searchType === 'address') {
                patronSearch.placeholder = 'Search by address...';
            }
            
            console.log('Placeholder updated to:', patronSearch.placeholder);
            
            // Clear search and results when changing type
            patronSearch.value = '';
            selectedPatronId.value = '';
            patronInfoCard.style.display = 'none';
            visitCountSection.style.display = 'none';
            patronResults.classList.remove('show');
            selectedIndex = -1;
            currentPatron = null;
        });
        
        // Autocomplete search functionality with smart matching
        let selectedIndex = -1;
        
        patronSearch.addEventListener('input', function() {
            const searchTerm = this.value.trim();
            const searchType = searchTypeSelect.value;
            
            console.log('Search input:', searchTerm, 'Type:', searchType);
            
            if (searchTerm.length === 0) {
                patronResults.classList.remove('show');
                selectedPatronId.value = '';
                patronInfoCard.style.display = 'none';
                visitCountSection.style.display = 'none';
                currentPatron = null;
                return;
            }
            
            // Filter patrons based on search type and logic
            const matches = filterPatrons(searchTerm, searchType);
            console.log('Matches found:', matches.length);
            
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
                // Check if starts with * for partial match
                if (lowerSearchTerm.startsWith('*')) {
                    const partialTerm = lowerSearchTerm.substring(1);
                    return patrons.filter(patron => 
                        patron.last_name.toLowerCase().includes(partialTerm)
                    );
                } else {
                    // Default: starts with search term
                    return patrons.filter(patron => 
                        patron.last_name.toLowerCase().startsWith(lowerSearchTerm)
                    );
                }
            } else if (searchType === 'first_name') {
                // Partial match for first name
                return patrons.filter(patron => 
                    patron.first_name.toLowerCase().includes(lowerSearchTerm)
                );
            } else if (searchType === 'address') {
                // Partial match for address
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
        
        // Display no results message
        function displayNoResults() {
            patronResults.innerHTML = '<div class="autocomplete-no-results">No matching patrons found</div>';
            patronResults.classList.add('show');
        }
        
        // Select a patron and auto-populate
        function selectPatron(patron) {
            console.log('Patron selected:', patron);
            
            currentPatron = patron; // Store for editing
            
            patronSearch.value = `${patron.last_name}, ${patron.first_name}`;
            selectedPatronId.value = patron.id;
            patronResults.classList.remove('show');
            
            // Display patron info card
            displayPatronInfo(patron);
            
            // Auto-populate from last visit if available
            if (patron.last_visit) {
                console.log('Auto-populating from last visit');
                zipcodeInput.value = patron.last_visit.zipcode;
                householdSizeInput.value = patron.last_visit.household_size;
                age0_18Input.value = patron.last_visit.age_0_18;
                age19_59Input.value = patron.last_visit.age_19_59;
                age60PlusInput.value = patron.last_visit.age_60_plus;
            } else {
                // Just populate zipcode if no last visit
                console.log('No last visit, populating zipcode only');
                zipcodeInput.value = patron.zipcode;
            }
            
            // Display visit count and last visit date
            displayVisitCount(patron);
        }
        
        // Display patron information card
        function displayPatronInfo(patron) {
            patronInfoName.textContent = `${patron.last_name}, ${patron.first_name}`;
            patronInfoAddress.textContent = patron.address || 'Not provided';
            
            // City and State
            const cityState = [];
            if (patron.city) cityState.push(patron.city);
            if (patron.state) cityState.push(patron.state);
            patronInfoCityState.textContent = cityState.length > 0 ? cityState.join(', ') : 'Not provided';
            
            patronInfoZip.textContent = patron.zipcode;
            
            // Comments (only show if exists)
            if (patron.comments) {
                patronInfoComments.textContent = patron.comments;
                patronInfoCommentsRow.style.display = 'flex';
            } else {
                patronInfoCommentsRow.style.display = 'none';
            }
            
            patronInfoCard.style.display = 'block';
        }
        
        // Display visit count for selected patron
        function displayVisitCount(patron) {
            console.log('Displaying visit count:', patron.visits_this_month);
            
            if (patron.visits_this_month !== undefined && patron.last_visit_date) {
                const count = patron.visits_this_month;
                const visitStatusText = document.getElementById('visitStatusText');
                
                if (count === 0) {
                    visitStatusText.textContent = '1st visit of the month';
                } else if (count === 1) {
                    visitStatusText.textContent = 'Visit #2 this month';
                } else {
                    visitStatusText.textContent = `Visit #${count + 1} this month`;
                }
                
                document.getElementById('lastVisitDate').textContent = formatDate(patron.last_visit_date);
                visitCountSection.style.display = 'flex';
            } else if (patron.visits_this_month === 0) {
                // First visit ever
                const visitStatusText = document.getElementById('visitStatusText');
                visitStatusText.textContent = '1st visit of the month';
                document.getElementById('lastVisitDate').textContent = 'Never';
                visitCountSection.style.display = 'flex';
            } else {
                visitCountSection.style.display = 'none';
            }
        }
        
        // Format date for display
        function formatDate(dateString) {
            // Parse the date string directly to avoid timezone issues
            const [year, month, day] = dateString.split('-');
            const date = new Date(year, month - 1, day); // month is 0-indexed in JS
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
        
        // Edit patron button click
        editPatronBtn.addEventListener('click', function() {
            if (currentPatron) {
                populateEditModal(currentPatron);
                editPatronModal.show();
            }
        });
        
        // Populate edit modal with patron data
        function populateEditModal(patron) {
            document.getElementById('editPatronId').value = patron.id;
            document.getElementById('editFirstName').value = patron.first_name;
            document.getElementById('editLastName').value = patron.last_name;
            document.getElementById('editAddress').value = patron.address || '';
            document.getElementById('editCity').value = patron.city || '';
            document.getElementById('editState').value = patron.state || '';
            document.getElementById('editZipcode').value = patron.zipcode;
            document.getElementById('editPhone').value = patron.phone || '';
            document.getElementById('editComments').value = patron.comments || '';
        }
        
        // Save patron changes via AJAX
        savePatronBtn.addEventListener('click', function() {
            const patronId = document.getElementById('editPatronId').value;
            const formData = {
                first_name: document.getElementById('editFirstName').value,
                last_name: document.getElementById('editLastName').value,
                address: document.getElementById('editAddress').value,
                city: document.getElementById('editCity').value,
                state: document.getElementById('editState').value,
                zipcode: document.getElementById('editZipcode').value,
                phone: document.getElementById('editPhone').value,
                comments: document.getElementById('editComments').value
            };
            
            // Get CSRF token
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            // Send AJAX request
            fetch(`/patron/${patronId}/edit-ajax/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update current patron object
                    currentPatron = { ...currentPatron, ...formData };
                    
                    // Update patron in patrons array
                    const index = patrons.findIndex(p => p.id == patronId);
                    if (index !== -1) {
                        patrons[index] = { ...patrons[index], ...formData };
                    }
                    
                    // Refresh patron info card
                    displayPatronInfo(currentPatron);
                    
                    // Update search display
                    patronSearch.value = `${formData.last_name}, ${formData.first_name}`;
                    
                    // Close modal
                    editPatronModal.hide();
                    
                    // Show success message
                    showToast('Patron updated successfully!', 'success');
                } else {
                    showToast('Error updating patron. Please try again.', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('Error updating patron. Please try again.', 'error');
            });
        });
        
        // Simple toast notification
        function showToast(message, type) {
            const toast = document.createElement('div');
            toast.className = `alert alert-${type === 'success' ? 'success' : 'danger'} position-fixed top-0 start-50 translate-middle-x mt-3`;
            toast.style.zIndex = '9999';
            toast.textContent = message;
            document.body.appendChild(toast);
            
            setTimeout(() => {
                toast.remove();
            }, 3000);
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
        // const ageInputs = [age0_18Input, age19_59Input, age60PlusInput];
        
        // ageInputs.forEach(input => {
        //     if (input) {
        //         input.addEventListener('input', function() {
        //             const total = ageInputs.reduce((sum, inp) => {
        //                 return sum + (parseInt(inp.value) || 0);
        //             }, 0);
                    
        //             if (total > 0) {
        //                 householdSizeInput.value = total;
        //             }
        //         });
        //     }
        // });

        // Restore patron selection if form had errors
        const preselectedPatronId = selectedPatronId.value;
        if (preselectedPatronId) {
            const patron = patrons.find(p => p.id == preselectedPatronId);
            if (patron) {
                // Show patron info and search, but DON'T auto-populate form fields
                patronSearch.value = `${patron.last_name}, ${patron.first_name}`;
                displayPatronInfo(patron);
                displayVisitCount(patron);
                // Don't call selectPatron() because that would overwrite the form values
            }
        }
    });
})();