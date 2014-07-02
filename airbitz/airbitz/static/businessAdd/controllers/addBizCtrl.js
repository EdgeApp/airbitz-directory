/* jshint devel:true */
var app = angular.module('addBiz');


app.controller('addBizCtrl', ['$scope', 'abDataFactory', '$state', function ($scope, abDataFactory, $state) {
  $scope.DF = abDataFactory;
  $scope.storage_array = $scope.DF.getData();

  $scope.init = function() {
    $('#google_places_autocomplete').focus();
  };

  // trying to watch globally accessible data
  $scope.$watch('storage_array', function() {
    console.log('STORAGE_ARRAY CHANGED');
  });


  $scope.lookupUpdate = function() {
    // write google autocomplete details to globally accessible storage_array
    $scope.DF.updateData($scope.details);
    $state.go('collectAll');
  };


  $scope.init();


}]);