/* jshint devel:true */
var app = angular.module('addBiz');


app.controller('collectAllInfo', ['$scope', 'abDataFactory', function($scope, abDataFactory) {
  console.log('collectAllInfo LOAAAAADED');
  $scope.DF = abDataFactory;
  $scope.storage_array = $scope.DF.getData();

  $scope.biz = $scope.storage_array[0];

}]);