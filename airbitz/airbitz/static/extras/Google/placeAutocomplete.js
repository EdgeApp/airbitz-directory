// Including this file will hook up a google autocomplte field to the #autocomplete input field
//

initializePlaceAutocomplete();

// Use the autocomplete feature of the Google Places API to help fill in the address info.
var autocomplete;
var origInputValues = {}
var componentForm = {
    street_number: 'short_name',
    route: 'long_name',
    locality: 'long_name',
    administrative_area_level_1: 'short_name',
    administrative_area_level_2: 'short_name',
    country: 'long_name',
    postal_code: 'short_name'
};

function initializePlaceAutocomplete() {
    // Create the autocomplete object, restricting the search
    // to geographical location types and establishments
    autocomplete = new google.maps.places.Autocomplete(
    /** @type {HTMLInputElement} */(document.getElementById('autocomplete')),
        { types: ['geocode', 'establishment'] });
    // When the user selects an address from the dropdown,
    // populate the address fields in the form
    google.maps.event.addListener(autocomplete, 'place_changed', function() {
        fillInAddress();
    });
    // If undo button or lookup elements exist add listener
    if (document.getElementById('undoAutocomplete')) {
        document.getElementById('undoAutocomplete').addEventListener('click', function() {
            inputsUndo();
        }, false);
    }
    if (document.getElementById('lookupName')) {
        document.getElementById('lookupName').addEventListener('click', function() {
            lookupName();
        }, false);
    }
}

function formatStreetAddress(streetAddress) {
	// Take street address components and combine them if both exist otherwise just use street
	if (streetAddress[0] && streetAddress[1]) {
		return streetAddress[0] + ' ' + streetAddress[1];
	}
	else if (streetAddress[1]) {
		return streetAddress[1];
	}
}

function setInputValue(cssId, inputValue) {
    if (typeof inputValue == 'undefined') { inputValue = '' }
    document.getElementById(cssId).value = inputValue;
}

function lookupName() {
    document.getElementById('autocomplete').value = document.getElementById('name').value
}

function inputsUndo() {
    for (var i=0; i < Object.keys(origInputValues).length; i++) {
        var elementId = Object.keys(origInputValues)[i];
        document.getElementById(elementId).value = origInputValues[elementId];
    }
    document.getElementById('autocomplete').value = '';
}

function holdInputForUndo(cssId) {
    if (document.getElementById(cssId)){
        var val = document.getElementById(cssId).value;
        origInputValues[cssId] = val;
    }
}

function holdInputsForUndo() {
    holdInputForUndo('address'); // street address
    holdInputForUndo('admin3_name'); // city
    holdInputForUndo('admin2_name'); // county
    holdInputForUndo('admin1_code'); // state
    holdInputForUndo('postalcode'); // zip
    holdInputForUndo('country'); // country
    holdInputForUndo('latitude'); // country
    holdInputForUndo('longitude'); // country
}

function fillInAddress() {
    // Get the place details from the autocomplete object
    var place = autocomplete.getPlace();
    var street_address = [];
    var admin3_name, admin2_name, admin1_code, postalcode, country, latitude, longitude;

    console.log(place);

    for (var component in componentForm) {
        if (document.getElementById(component)) {
            document.getElementById(component).value = '';
            document.getElementById(component).disabled = false;
        }
    }

    // Get each component of the address from the place details
    // and get the corresponding values to set the inputs to
    for (var i = 0; i < place.address_components.length; i++) {
        var addressType = place.address_components[i].types[0];

        if (addressType == 'street_number') {
            street_address[0] = place.address_components[i][componentForm[addressType]];
        }
        if (addressType == 'route') {
            street_address[1] = place.address_components[i][componentForm[addressType]];
        }
        if (addressType == 'locality') {
            // City
            admin3_name = place.address_components[i][componentForm[addressType]];
        }
        if (addressType == 'administrative_area_level_2') {
            // County
            admin2_name = place.address_components[i][componentForm[addressType]];
        }
        if (addressType == 'administrative_area_level_1') {
            // State
            admin1_code = place.address_components[i][componentForm[addressType]];
        }
        if (addressType == 'postal_code') {
            // Zip
            postalcode = place.address_components[i][componentForm[addressType]];
        }
        if (addressType == 'country') {
            // Country
            country = place.address_components[i][componentForm[addressType]];
        }

        // automaitc value mappings for fields named identical to the api
        if (componentForm[addressType]) {
            if (document.getElementById(addressType)) {
                var val = place.address_components[i][componentForm[addressType]];
                document.getElementById(addressType).value = val;
            }
        }
    }

    holdInputsForUndo();

    // Clear address fields
    document.getElementById('address').value = '';
    setInputValue('address', formatStreetAddress(street_address)); // street address
    setInputValue('admin3_name', admin3_name); // city
    setInputValue('admin2_name', admin2_name); // county
    setInputValue('admin1_code', admin1_code); // state
    setInputValue('postalcode', postalcode); // zip
    setInputValue('country', country); // country
    setInputValue('latitude', place.geometry.location.lat().toFixed(7)); // country
    setInputValue('longitude', place.geometry.location.lng().toFixed(7)); // country
}