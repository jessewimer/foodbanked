// Visit Form JavaScript with Enhanced Search, Patron Info Display, and Inline Editing
(function() {
    'use strict';
    
    // Parse patron data from script tag
    const patronDataElement = document.getElementById('patronData');
    let patrons = patronDataElement ? JSON.parse(patronDataElement.textContent) : [];
    
    // Store currently selected patron for editing
    let currentPatron = null;
    
    document.addEventListener('DOMContentLoaded', function() {

        // Check if we have patron data in the URL (from creating new patron)
        const urlParams = new URLSearchParams(window.location.search);
        const patronId = urlParams.get('patron_id');
 
        // Service zipcodes data (passed from backend)
        const serviceZipcodes = JSON.parse(document.getElementById('serviceZipcodesData')?.textContent || '[]');
        // Check if serviceZipcodes is defined and has data
        console.log('Service zipcodes loaded:', serviceZipcodes);
        console.log('Number of zipcodes:', serviceZipcodes ? serviceZipcodes.length : 'undefined');
        const validStates = [
            'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
            'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
            'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
            'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
            'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
            'DC'
        ];

        // hide city/state/zip row if by name is default mode
        const addressRow = document.getElementById('addressRow');
        if (addressRow) {
            addressRow.style.display = 'none';
        }
        
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
    
        // Form fields
        const zipcodeInput = document.getElementById('id_zipcode');
        const zipcodeResults = document.getElementById('zipcodeResults');
        const cityInput = document.getElementById('id_city');
        const stateInput = document.getElementById('id_state');
        const householdSizeInput = document.getElementById('id_household_size');
        const age0_18Input = document.getElementById('id_age_0_18');
        const age19_59Input = document.getElementById('id_age_19_59');
        const age60PlusInput = document.getElementById('id_age_60_plus');
        
        // Visit count section
        const visitCountSection = document.getElementById('visitCountSection');
        const firstVisitSection = document.getElementById('firstVisitSection');
        let isSwitchingMode = false;
        // Handle visit type toggle
        const visitTypeRadios = document.querySelectorAll('input[name="visitType"]');
        
        const allowByName = form.dataset.allowByName === 'true';
        const allowAnonymous = form.dataset.allowAnonymous === 'true';

        
        // Check initial state on page load
        const initialChecked = document.querySelector('input[name="visitType"]:checked');


        
        // Age group inputs for auto-calculation
        const ageInputs = [age0_18Input, age19_59Input, age60PlusInput];

        function updateHouseholdSize() {
            let total = 0;
            ageInputs.forEach(input => {
                const value = parseInt(input.value) || 0;
                total += value;
            });
            householdSizeInput.value = total;
        }

        // Add event listeners to age inputs
        ageInputs.forEach(input => {
            input.addEventListener('input', updateHouseholdSize);
        });

        // Calculate initial value on page load
        updateHouseholdSize();






        if (patronId) {
            // Build patron object from URL parameters (no API call needed!)
            const patronData = {
                id: parseInt(patronId),
                first_name: urlParams.get('first_name') || '',
                last_name: urlParams.get('last_name') || '',
                zipcode: urlParams.get('zipcode') || '',
                city: urlParams.get('city') || '',
                state: urlParams.get('state') || '',
                address: urlParams.get('address') || '',
                comments: urlParams.get('comments') || '',
                last_visit: null,  // New patron has no visits
                visit_count: 0,
                visits_this_month: 0,
                last_visit_date: null
            };
            
            // Call the existing selectPatron function immediately
            selectPatron(patronData);
            
            // Clean up URL (remove all patron parameters)
            window.history.replaceState({}, '', window.location.pathname);
        }


        if (allowByName && allowAnonymous) {
            // Both enabled - normal behavior
            if (initialChecked && initialChecked.value === 'anonymous') {
                patronSearchSection.style.display = 'none';
                patronInfoCard.style.display = 'none';
                visitCountSection.style.display = 'none';
                firstVisitSection.style.display = 'block';

                const addressRow = document.getElementById('addressRow');
                if (addressRow) {
                    addressRow.style.display = '';
                }
            } else {
                // By Name selected on load (default) - hide address fields
                const addressRow = document.getElementById('addressRow');
                if (addressRow) {
                    addressRow.style.display = 'none';
                }
            }
                        
            // Radio button change handlers (only needed when both are enabled)
            visitTypeRadios.forEach(radio => {
                radio.addEventListener('change', function() {
                    
                    if (this.value === 'anonymous') {
                        isSwitchingMode = true;
                        // Hide patron-related sections
                        patronSearchSection.style.display = 'none';
                        patronInfoCard.style.display = 'none';
                        visitCountSection.style.display = 'none';
                        
                        // Show anonymous-specific sections
                        firstVisitSection.style.display = 'block';
                        
                        // Show the zip/city/state row for manual entry
                        const addressRow = document.getElementById('addressRow');
                        if (addressRow) {
                            addressRow.style.display = '';
                        }
                        
                        // Clear patron selection
                        patronSearch.value = '';
                        selectedPatronId.value = '';
                        patronResults.classList.remove('show');
                        currentPatron = null;
                        
                        // Clear all form fields
                        clearFormFields();
                        setTimeout(() => { isSwitchingMode = false; }, 100);
                        
                    } else {
                        // Show patron search section
                        patronSearchSection.style.display = 'block';
                        
                        // Hide anonymous-specific sections
                        firstVisitSection.style.display = 'none';
                        patronInfoCard.style.display = 'none';
                        visitCountSection.style.display = 'none';

                        // Hide the zip/city/state row (address comes from patron profile)
                        const addressRow = document.getElementById('addressRow');
                        if (addressRow) {
                            addressRow.style.display = 'none';
                        }
                        // Clear all form fields
                        clearFormFields();
                    }
                    
                });
            });
            
        } else if (allowByName && !allowAnonymous) {
            // Only by name enabled - always show patron search
            if (patronSearchSection) patronSearchSection.style.display = 'block';
            if (firstVisitSection) firstVisitSection.style.display = 'none';
            const addressRow = document.getElementById('addressRow');
            if (addressRow) {
                addressRow.style.display = 'none';
            }
            
        } else if (!allowByName && allowAnonymous) {
            // Only anonymous enabled - hide patron search, show first visit
            if (patronSearchSection) patronSearchSection.style.display = 'none';
            if (patronInfoCard) patronInfoCard.style.display = 'none';
            if (visitCountSection) visitCountSection.style.display = 'none';
            if (firstVisitSection) firstVisitSection.style.display = 'block';
            const addressRow = document.getElementById('addressRow');
            if (addressRow) {
                addressRow.style.display = '';
            }
        }


        function clearFormFields() {
            
            if (zipcodeInput) {
                zipcodeInput.value = '';
            }
            if (cityInput) {
                cityInput.value = '';
            }
            if (stateInput) {
                stateInput.value = '';
            }
            if (householdSizeInput) householdSizeInput.value = '1';
            if (age0_18Input) age0_18Input.value = '0';
            if (age19_59Input) age19_59Input.value = '0';
            if (age60PlusInput) age60PlusInput.value = '0';
            const firstVisitCheckbox = document.getElementById('id_first_visit_this_month');
            if (firstVisitCheckbox) firstVisitCheckbox.checked = false;
        }


        if (initialChecked && initialChecked.value === 'anonymous') {
            console.log('Setting anonymous mode on load');
            patronSearchSection.style.display = 'none';
            patronInfoCard.style.display = 'none';
            visitCountSection.style.display = 'none';
            firstVisitSection.style.display = 'block';
        }

        
        searchTypeSelect.addEventListener('change', function() {
            const value = this.value;
            
            // Update hidden field
            document.getElementById('searchTypeHidden').value = value;
            
            if (value === 'anonymous') {
                patronSearchSection.style.display = 'none';
                clearPatronSelection();
                // Clear all form fields
                clearFormFields();
            } else {
                patronSearchSection.style.display = 'block';
                updateSearchPlaceholder();
                clearPatronSelection();
                // Clear all form fields
                clearFormFields();
                patronSearch.focus();
            }
            
            patronResults.style.display = 'none';
            patronSearch.value = '';
            selectedIndex = -1;
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
            
            currentPatron = patron; // Store for editing
            selectedPatronId.value = patron.id;
            // Update patron info card
            patronInfoName.textContent = `${patron.first_name} ${patron.last_name}`;
            patronInfoAddress.textContent = patron.address || 'Not provided';
            patronInfoCityState.textContent = patron.city && patron.state 
                ? `${patron.city}, ${patron.state}` 
                : 'Not provided';
            patronInfoZip.textContent = patron.zipcode || 'Not provided';
            // Auto-populate hidden address fields
            if (zipcodeInput) zipcodeInput.value = patron.zipcode || '';
            if (cityInput) cityInput.value = patron.city || '';
            if (stateInput) stateInput.value = patron.state || '';

            // Hide the zip/city/state row since it's shown in patron card
            const addressRow = document.getElementById('addressRow');
            if (addressRow) {
                addressRow.style.display = 'none';
            }

            patronResults.classList.remove('show');
            
            // Display patron info card
            displayPatronInfo(patron);
            
            // Auto-populate from last visit if available
            if (patron.last_visit) {
                householdSizeInput.value = patron.last_visit.household_size;
                age0_18Input.value = patron.last_visit.age_0_18;
                age19_59Input.value = patron.last_visit.age_19_59;
                age60PlusInput.value = patron.last_visit.age_60_plus;
            } else {
                // Just populate zipcode if no last visit
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
                    
                    // Update the hidden form fields with new address data
                    if (zipcodeInput) zipcodeInput.value = currentPatron.zipcode || '';
                    if (cityInput) cityInput.value = currentPatron.city || '';
                    if (stateInput) stateInput.value = currentPatron.state || '';
                    
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
      
        // RESTORE STATE AFTER VALIDATION ERROR
        const formStateElement = document.getElementById('formStateData');
        if (formStateElement) {
            const formState = JSON.parse(formStateElement.textContent);
            const selectedPatronIdFromServer = formState.selected_patron_id;
            const searchTypeFromServer = formState.search_type;

            // ONLY restore if search_type exists (means validation error occurred)
            if (searchTypeFromServer) {
                if (searchTypeFromServer === 'anonymous') {
                    // Restore anonymous mode
                    searchTypeSelect.value = 'anonymous';
                    patronSearchSection.style.display = 'none';
                    document.getElementById('searchTypeHidden').value = 'anonymous';
                } else {
                    // Restore "By Name" mode
                    const dropdownValue = searchTypeFromServer === 'name' ? 'last_name' : searchTypeFromServer;
                    searchTypeSelect.value = dropdownValue;
                    patronSearchSection.style.display = 'block';
                    updateSearchPlaceholder();
                    document.getElementById('searchTypeHidden').value = searchTypeFromServer;
                    
                    // Restore patron if one was selected
                    if (selectedPatronIdFromServer) {
                        const patron = patrons.find(p => p.id === parseInt(selectedPatronIdFromServer));
                        if (patron) {
                            selectPatron(patron);
                        }
                    }
                }
            }
        }

        // Validate visit type checkboxes when food truck is enabled
        const visitForm = document.getElementById('visitForm');
        if (visitForm) {
            visitForm.addEventListener('submit', function(e) {
                // First, run our custom validation
                if (!validateForm()) {
                    e.preventDefault();
                    return false;
                }
            });
        }

        let selectedZipcodeIndex = -1;

        if (zipcodeInput && zipcodeResults) {
            // Show all zipcodes on focus
            zipcodeInput.addEventListener('focus', function() {
                if (!isSwitchingMode && serviceZipcodes.length > 0) {
                    displayZipcodeResults(serviceZipcodes);
                }
            });
            
            // Filter zipcodes as user types
            zipcodeInput.addEventListener('input', function() {
                const query = this.value.toLowerCase();
                
                if (query === '') {
                    displayZipcodeResults(serviceZipcodes);
                } else {
                    const filtered = serviceZipcodes.filter(z => 
                        z.zipcode.toLowerCase().includes(query) ||
                        z.city.toLowerCase().includes(query)
                    );
                    displayZipcodeResults(filtered);
                }
            });
            
            // Keyboard navigation
            zipcodeInput.addEventListener('keydown', function(e) {
                const items = zipcodeResults.querySelectorAll('.autocomplete-item');
                
                if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    selectedZipcodeIndex = Math.min(selectedZipcodeIndex + 1, items.length - 1);
                    updateZipcodeSelection(items);
                } else if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    selectedZipcodeIndex = Math.max(selectedZipcodeIndex - 1, -1);
                    updateZipcodeSelection(items);
                } else if (e.key === 'Enter' && selectedZipcodeIndex >= 0) {
                    e.preventDefault();
                    items[selectedZipcodeIndex].click();
                } else if (e.key === 'Escape') {
                    zipcodeResults.style.display = 'none';
                    selectedZipcodeIndex = -1;
                }
            });
            
            // Hide results when clicking outside
            document.addEventListener('click', function(e) {
                if (!zipcodeInput.contains(e.target) && !zipcodeResults.contains(e.target)) {
                    zipcodeResults.style.display = 'none';
                    selectedZipcodeIndex = -1;
                }
            });
        }


        function validateForm() {
            let isValid = true;
            const errors = [];
            const patronCardErrors = [];
            
            // Clear previous errors
            document.querySelectorAll('.field-error').forEach(el => el.classList.remove('field-error', 'error-shake'));
            document.querySelectorAll('.error-message').forEach(el => el.remove());
            
            // Clear patron card error if it exists
            const existingPatronError = document.getElementById('patron-card-error');
            if (existingPatronError) {
                existingPatronError.remove();
            }
            if (patronInfoCard) {
                patronInfoCard.classList.remove('error-shake');
            }
            
            // Check if address fields are hidden (patron is selected)
            const addressFieldsHidden = addressRow && addressRow.style.display === 'none';
            
            // Helper function to show error
            function showError(input, message, forcePatronCard = false) {
                isValid = false;
                
                // If address fields are hidden OR forcePatronCard, save for patron card
                if (addressFieldsHidden || forcePatronCard) {
                    patronCardErrors.push(message);
                } else {
                    // Show error on the field itself
                    input.classList.add('field-error', 'error-shake');
                    
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'error-message';
                    errorDiv.textContent = message;
                    
                    // Insert error message after the input
                    input.parentNode.insertBefore(errorDiv, input.nextSibling);
                    
                    errors.push({ element: input, message: message });
                }
            }
            
            // Validate Zipcode (must be exactly 5 digits)
            const zipcodeValue = zipcodeInput.value.trim();
            if (!zipcodeValue) {
                showError(zipcodeInput, 'Zip code is required');
            } else if (!/^\d{5}$/.test(zipcodeValue)) {
                showError(zipcodeInput, 'Zip code must be exactly 5 digits');
            }
            
            // Validate City (must be present)
            const cityValue = cityInput.value.trim();
            if (!cityValue) {
                showError(cityInput, 'City is required');
            }
            
            // Validate State (must be present and valid)
            const stateValue = stateInput.value.trim().toUpperCase();
            if (!stateValue) {
                showError(stateInput, 'State is required');
            } else if (!validStates.includes(stateValue)) {
                showError(stateInput, 'Please enter a valid 2-letter state code (e.g., ID, WA, OR)');
            }
            
            // Validate Household Size (must be at least 1)
            const householdSize = parseInt(householdSizeInput.value) || 0;
            if (householdSize < 1) {
                showError(householdSizeInput, 'Household size must be at least 1');
            }
            
            // Validate Age Groups (must add up to household size)
            const age0_18 = parseInt(age0_18Input.value) || 0;
            const age19_59 = parseInt(age19_59Input.value) || 0;
            const age60Plus = parseInt(age60PlusInput.value) || 0;
            const totalAges = age0_18 + age19_59 + age60Plus;
            if (totalAges !== householdSize) {
                const ageGroupsSection = document.querySelector('.age-groups');
                if (ageGroupsSection) {
                    isValid = false;
                    ageGroupsSection.classList.add('field-error', 'error-shake');
                    
                    // Remove any existing error message in age groups
                    const existingError = ageGroupsSection.querySelector('.error-message');
                    if (existingError) existingError.remove();
                    
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'error-message';
                    errorDiv.style.marginTop = '0.75rem';
                    errorDiv.textContent = `Age groups must add up to household size (${householdSize}). Currently adds to ${totalAges}.`;
                    
                    ageGroupsSection.appendChild(errorDiv);
                    
                    errors.push({ element: ageGroupsSection, message: errorDiv.textContent });
                }
            }
            
            // If we have patron card errors, display them on the patron card
            if (patronCardErrors.length > 0 && patronInfoCard) {
                const patronCardError = document.createElement('div');
                patronCardError.id = 'patron-card-error';
                patronCardError.className = 'alert alert-danger mt-3';
                patronCardError.innerHTML = '<strong>Missing Information:</strong><br>' + patronCardErrors.join('<br>');
                
                patronInfoCard.appendChild(patronCardError);
                patronInfoCard.classList.add('error-shake');
                
                // Scroll to patron card
                patronInfoCard.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'center' 
                });
            } else if (!isValid && errors.length > 0) {
                // If there are regular field errors, scroll to the first error
                errors[0].element.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'center' 
                });
                errors[0].element.focus();
            }

            // Validate Food Truck vs Pantry (only if food truck is enabled)
            const foodTruckCheckbox = document.getElementById('visitTypeFoodTruck');
            const pantryCheckbox = document.getElementById('visitTypePantry');

            if (foodTruckCheckbox && pantryCheckbox) {
                // Food truck feature is enabled, check if at least one is selected
                if (!foodTruckCheckbox.checked && !pantryCheckbox.checked) {
                    const visitTypeSection = document.querySelector('.visit-type-checkboxes').parentElement;
                    if (visitTypeSection) {
                        isValid = false;
                        visitTypeSection.classList.add('error-shake');
                        
                        // Remove any existing error message
                        const existingError = visitTypeSection.querySelector('.error-message');
                        if (existingError) existingError.remove();
                        
                        const errorDiv = document.createElement('div');
                        errorDiv.className = 'error-message';
                        errorDiv.style.marginTop = '0.5rem';
                        errorDiv.textContent = 'Please select at least one visit type (Pantry or Food Truck)';
                        
                        visitTypeSection.appendChild(errorDiv);
                        
                        errors.push({ element: visitTypeSection, message: errorDiv.textContent });
                    }
                }
            }
            
            return isValid;
        }


        // Auto-populate city/state based on zipcode (for anonymous mode)
        if (zipcodeInput && cityInput && stateInput) {
            zipcodeInput.addEventListener('input', function() {
                const zipValue = this.value.trim();
                
                // Only trigger when we have exactly 5 digits
                if (zipValue.length === 5 && /^\d{5}$/.test(zipValue)) {
                    autopopulateCityState(zipValue);
                } else {
                    // Clear the dropdown if zipcode is incomplete
                    const cityStateResults = document.getElementById('cityStateResults');
                    if (cityStateResults) {
                        cityStateResults.style.display = 'none';
                    }
                }
            });
            
            // Also trigger on blur to catch paste events
            zipcodeInput.addEventListener('blur', function() {
                const zipValue = this.value.trim();
                if (zipValue.length === 5 && /^\d{5}$/.test(zipValue)) {
                    setTimeout(() => autopopulateCityState(zipValue), 100);
                }
            });
        }

        // Add a flag to prevent re-triggering
        let isSelectingFromDropdown = false;

        function autopopulateCityState(zipcode) {
            // Don't auto-populate if user is selecting from dropdown
            if (isSelectingFromDropdown) return;
            
            console.log('autopopulateCityState called with:', zipcode);
            console.log('Available service zipcodes:', serviceZipcodes);
            
            // Find all matching zipcodes
            const matches = serviceZipcodes.filter(z => z.zipcode === zipcode);
            console.log('Matches found:', matches);
            
            const cityStateResults = document.getElementById('cityStateResults');
            console.log('cityStateResults element:', cityStateResults);
            
            if (!cityStateResults) {
                console.error('cityStateResults element not found!');
                return;
            }
            
            if (matches.length === 0) {
                // No matches found - clear fields and hide dropdown
                cityStateResults.style.display = 'none';
                return;
            } else if (matches.length === 1) {
                // Single match - auto-populate directly
                cityInput.value = matches[0].city;
                stateInput.value = matches[0].state;
                cityStateResults.style.display = 'none';
            } else {
                // Multiple matches - show dropdown
                displayCityStateOptions(matches);
            }
        }

        function displayCityStateOptions(matches) {
            const cityStateResults = document.getElementById('cityStateResults');
            if (!cityStateResults) return;
            
            cityStateResults.innerHTML = '';
            
            matches.forEach((match, index) => {
                const item = document.createElement('div');
                item.className = 'city-state-item';
                item.dataset.city = match.city;
                item.dataset.state = match.state;
                
                item.innerHTML = `
                    <div class="city-state-city">${match.city}</div>
                    <div class="city-state-details">Zipcode: ${match.zipcode} • State: ${match.state}</div>
                `;
                
                item.addEventListener('click', function(e) {
                    e.stopPropagation(); // Prevent event bubbling
                    isSelectingFromDropdown = true; // Set flag
                    
                    cityInput.value = this.dataset.city;
                    stateInput.value = this.dataset.state;
                    cityStateResults.style.display = 'none';
                    
                    // Remove focus styling from all items
                    cityStateResults.querySelectorAll('.city-state-item').forEach(i => {
                        i.classList.remove('selected');
                    });
                    
                    // Reset flag after a short delay
                    setTimeout(() => {
                        isSelectingFromDropdown = false;
                    }, 100);
                });
                
                // Keyboard navigation
                item.addEventListener('mouseenter', function() {
                    cityStateResults.querySelectorAll('.city-state-item').forEach(i => {
                        i.classList.remove('selected');
                    });
                    this.classList.add('selected');
                });
                
                cityStateResults.appendChild(item);
            });
            
            cityStateResults.style.display = 'block';
            
            // Auto-select first item
            const firstItem = cityStateResults.querySelector('.city-state-item');
            if (firstItem) {
                firstItem.classList.add('selected');
            }
        }

        // Hide city/state dropdown when clicking outside
        document.addEventListener('click', function(e) {
            const cityStateResults = document.getElementById('cityStateResults');
            if (cityStateResults && 
                !cityStateResults.contains(e.target) && 
                e.target !== zipcodeInput && 
                e.target !== cityInput && 
                e.target !== stateInput) {
                cityStateResults.style.display = 'none';
            }
        });

        // Add keyboard navigation for city/state dropdown
        if (zipcodeInput) {
            zipcodeInput.addEventListener('keydown', function(e) {
                const cityStateResults = document.getElementById('cityStateResults');
                if (!cityStateResults || cityStateResults.style.display === 'none') return;
                
                const items = cityStateResults.querySelectorAll('.city-state-item');
                const selected = cityStateResults.querySelector('.city-state-item.selected');
                let currentIndex = Array.from(items).indexOf(selected);
                
                if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    currentIndex = Math.min(currentIndex + 1, items.length - 1);
                    items.forEach((item, idx) => {
                        item.classList.toggle('selected', idx === currentIndex);
                    });
                } else if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    currentIndex = Math.max(currentIndex - 1, 0);
                    items.forEach((item, idx) => {
                        item.classList.toggle('selected', idx === currentIndex);
                    });
                } else if (e.key === 'Enter' && selected) {
                    e.preventDefault();
                    selected.click();
                } else if (e.key === 'Escape') {
                    cityStateResults.style.display = 'none';
                }
            });
        }
            
    });
})();