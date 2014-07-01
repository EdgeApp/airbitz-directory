/* jshint devel:true */
var app = angular.module('addBiz');


app.controller('addBizCtrl', ['$scope', 'abDataFactory', function ($scope, abDataFactory) {
  $scope.DF = abDataFactory;
  $scope.storage_array = $scope.DF.getData();

  // trying to watch globally accessible data
  $scope.$watch('', function() {
    console.log('STORAGE_ARRAY CHANGED');
  });






}]);