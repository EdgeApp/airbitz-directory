/* jshint devel:true */
var app = angular.module('addBiz');


app.controller('generalInfoCtrl', ['$scope', 'abDataFactory', function($scope, abDataFactory) {
  console.log('generalInfo LOADED');
  $scope.DF = abDataFactory;
  $scope.storage_array = $scope.DF.getData();

  $scope.biz = $scope.storage_array[0];





}]);