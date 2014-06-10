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
    country: 'short_name',
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

function formatCounty(county) {
    if (county) {
        switch(county) {
            case 'Orange County':   return county;
            default:                return county.split(" County")[0]; // remove county
        }
    }
    return county;
}

function formatCountry(country) {
    if (country) {
        switch(country) {
            case 'GB':  return 'UK';
            default:    return country;
        }
    }
}

function setInputValue(cssId, inputValue) {
    if (document.getElementById(cssId)) {
        console.log('Setting value of: #' + cssId);

        var inputElement = document.getElementById(cssId);
        var origVal = inputElement.value;
        if (typeof inputValue == 'undefined') { inputValue = '' }

        if (origVal == inputValue) {
            return true;
        } else {
            inputElement.value = inputValue;

            // Show that fields were updated and when focused remove effect
            inputElement.className += ' updated-field';
            $('.updated-field').removeClass('undo-field');
            $('.updated-field').on('focus', function(){
                $(this).removeClass('updated-field');
            });
        }
    } else {
        console.log('setInputValue() failed to set value. Cannot find element: #' + cssId);
    }
}

function lookupName() {
    document.getElementById('autocomplete').value = document.getElementById('name').value;
}

function inputsUndo() {
    for (var i=0; i < Object.keys(origInputValues).length; i++) {
        var elementId = Object.keys(origInputValues)[i];
        document.getElementById(elementId).value = origInputValues[elementId];
    }
    document.getElementById('autocomplete').value = '';
    $('.updated-field').removeClass('updated-field');
}

function holdInputForUndo(cssId) {
    var inputElement = document.getElementById(cssId)
    if (inputElement){
        var val = inputElement.value;
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
    holdInputForUndo('phone'); // country
}

function fillInAddress() {
    // Get the place details from the autocomplete object
    var place = autocomplete.getPlace();
    var street_address = [];
    var admin3_name, admin2_name, admin1_code, postalcode, country, latitude, longitude, phone;

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

    // Get phone number if available
    if (place.formatted_phone_number) {
        phone = place.international_phone_number;
    }

    // Clear address fields
    document.getElementById('address').value = '';
    setInputValue('address', formatStreetAddress(street_address)); // street address
    setInputValue('admin3_name', admin3_name); // city
    setInputValue('admin2_name', formatCounty(admin2_name)); // county
    setInputValue('admin1_code', admin1_code); // state
    setInputValue('postalcode', postalcode); // zip
    setInputValue('country', formatCountry(country)); // country
    setInputValue('latitude', place.geometry.location.lat().toFixed(7)); // country
    setInputValue('longitude', place.geometry.location.lng().toFixed(7)); // country
    setInputValue('phone', phone); // phone

    updateLatLng();
}


function updateLatLng() {
    var lat = $('#latitude').val();
    var lng = $('#longitude').val();
    $('#latlng').val(lat + ',' + lng);
}

$('#latitude, #longitude').on('change', function(){
    updateLatLng();
});

$('.geocode-latlon').click(function(e) {
    var lat = $('#latitude').val();
    var lng = $('#longitude').val();
    var latlng = new google.maps.LatLng(lat, lng);

    var geocoder = new google.maps.Geocoder();

    geocoder.geocode({'latLng': latlng}, function(results, status) {
//        console.log('STATUS:' + status);

        if (status === 'OK' && results) {
            var street_address = [];

//            console.log('LENGTH: ' + results.length);

            for (var i = 0; i < results.length; i++) {
                var addressType = results[i].types[0];


                if (addressType == 'street_address') {

//                    console.log(addressType);
//                    console.log(results[i]);

                    street_address[0] = results[i].address_components[0].types[0]
                    street_address[1] = results[i].address_components[1]['long_name']

//                    console.log(results[i].address_components.length);

                    for (var j = 0; j < results[i].address_components.length; j++) {
                        var addressComponent = results[i].address_components[j];
                        var addressType = addressComponent.types[0]
//                        console.log(addressComponent);

                        if ( addressType == 'street_number') {
                            street_address[0] = addressComponent[componentForm[addressType]];
                        }
                        if ( addressType == 'route') {
                            street_address[1] = addressComponent[componentForm[addressType]];
                        }
                        if (addressType == 'locality') {
                            // City
                            admin3_name = addressComponent[componentForm[addressType]];
                        }
                        if (addressType == 'administrative_area_level_2') {
                            // County
                            admin2_name = addressComponent[componentForm[addressType]];
                        }
                        if (addressType == 'administrative_area_level_1') {
                            // State
                            admin1_code = addressComponent[componentForm[addressType]];
                        }
                        if (addressType == 'postal_code') {
                            // Zip
                            postalcode = addressComponent[componentForm[addressType]];
                        }
                        if (addressType == 'country') {
                            // Country
                            country = addressComponent[componentForm[addressType]];
                        }
                    }
                }
            }

            holdInputsForUndo();

            setInputValue('address', formatStreetAddress(street_address)); // street address
            setInputValue('admin3_name', admin3_name); // city
            setInputValue('admin2_name', formatCounty(admin2_name)); // county
            setInputValue('admin1_code', admin1_code); // state
            setInputValue('postalcode', postalcode); // zip
            setInputValue('country', country); // country
        }

    });

    e.preventDefault();
    return false;
});


$('.geocode-address').click(function(e) {
    var self = $(this);
    var origText = self.html();
    var address = $('#address').val();
    var city = $('#admin3_name').val();
    var state = $('#admin1_code').val();
    var zip = $('#postalcode').val();
    var self = jQuery(this);
    if (!address || !city || !state || !zip) {
        alert("Missing address fields. Unable to geocode address.");
        return false;
    }
    var address = address + ',' + city + ',' + state + ',' + zip
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode({'address': address}, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var loc = results[0].geometry;
            latestResult = results[0];
            var g = latestResult.geometry.location;
            console.log(g);
            $('#latitude').val(g.lat().toFixed(7));
            $('#longitude').val(g.lng().toFixed(7));
            updateLatLng();
        } else {
            alert('Unable to find lat/lon from ' + address);
        }
        self.html(origText);
    });

    e.preventDefault();
    return false;
});