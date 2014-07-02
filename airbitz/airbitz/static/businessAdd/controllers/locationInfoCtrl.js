/* jshint devel:true */
var app = angular.module('addBiz');


app.controller('locationInfoCtrl', ['$scope', 'abDataFactory', function($scope, abDataFactory) {
  console.log('locationInfoCtrl LOADED');
  $scope.DF = abDataFactory;
  $scope.storage_array = $scope.DF.getData();

  $scope.biz = $scope.storage_array[0];



  $scope.formatStreetAddress = function(streetAddress) {
    // Take street address components and combine them if both exist otherwise just use street
    if (streetAddress[0] && streetAddress[1]) {
      return streetAddress[0] + ' ' + streetAddress[1];
    }
    else if (streetAddress[1]) {
      return streetAddress[1];
    }
  };

  $scope.formatCounty = function(county) {
    if (county) {
      switch(county) {
        case 'Orange County':   return county;
        default:                return county.split(" County")[0]; // remove county
      }
    }
    return county;
  };

  $scope.formatCountry = function(country) {
    if (country) {
      switch(country) {
        case 'GB':  return 'UK';
        default:    return country;
      }
    }
  };

  $scope.parseAddress = function() {
    console.log('parseAddress CALLED');

    var componentForm = {
      street_number: 'short_name',
      route: 'long_name',
      locality: 'long_name',
      administrative_area_level_1: 'short_name',
      administrative_area_level_2: 'short_name',
      country: 'short_name',
      postal_code: 'short_name'
    };


    var street_address = [];
    var admin3_name, admin2_name, admin1_code, postalcode, country;

    // Get each component of the address from the place details
    // and get the corresponding values to set the inputs to
    for (var i = 0; i < $scope.biz.address_components.length; i++) {
      var addressType = $scope.biz.address_components[i].types[0];

      if (addressType == 'street_number') {
        street_address[0] = $scope.biz.address_components[i][componentForm[addressType]];
      }
      if (addressType == 'route') {
        street_address[1] = $scope.biz.address_components[i][componentForm[addressType]];
      }
      if (addressType == 'locality') {
        // City
        admin3_name = $scope.biz.address_components[i][componentForm[addressType]];
      }
      if (addressType == 'administrative_area_level_2') {
        // County
        admin2_name = $scope.biz.address_components[i][componentForm[addressType]];
      }
      if (addressType == 'administrative_area_level_1') {
        // State
        admin1_code = $scope.biz.address_components[i][componentForm[addressType]];
      }
      if (addressType == 'postal_code') {
        // Zip
        postalcode = $scope.biz.address_components[i][componentForm[addressType]];
      }
      if (addressType == 'country') {
        // Country
        country = $scope.biz.address_components[i][componentForm[addressType]];
      }
    }

    console.log('UPDATING LOCATION DATA-BINDINGS');
    $scope.biz.address = $scope.formatStreetAddress(street_address); // street address
    $scope.biz.admin3_name = admin3_name; // city
    $scope.biz.admin2_name = $scope.formatCounty(admin2_name); // county
    $scope.biz.admin1_code = admin1_code; // state
    $scope.biz.postalcode = postalcode; // zip
    $scope.biz.country =  $scope.formatCountry(country); // country


  };




  if($scope.biz) {
    if($scope.biz.address_components) {
      $scope.parseAddress();
      $scope.$broadcast('DATA_PARSED');
    }
  }


}]);