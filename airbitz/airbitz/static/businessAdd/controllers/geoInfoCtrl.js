/* jshint devel:true */
var app = angular.module('addBiz');


app.controller('geoInfoCtrl', ['$scope', 'abDataFactory', function($scope, abDataFactory) {
  console.log('geoInfoCtrl LOADED');
  $scope.DF = abDataFactory;
  $scope.storage_array = $scope.DF.getData();

  $scope.biz = $scope.storage_array[0];


  $scope.updateLatLng = function() {
    var lat = $scope.biz.latitude;
    var lng = $scope.biz.longitude;
    $scope.biz.latlng = lat + ',' + lng;
  }

  if($scope.biz) {
    if($scope.biz.geometry) {
      console.log('UPDATING GEO DATA-BINDINGS');
      $scope.biz.latitude = $scope.biz.geometry.location.lat().toFixed(7); // lat
      $scope.biz.longitude = $scope.biz.geometry.location.lng().toFixed(7); // long

      $scope.updateLatLng();
    }
  }

}]);