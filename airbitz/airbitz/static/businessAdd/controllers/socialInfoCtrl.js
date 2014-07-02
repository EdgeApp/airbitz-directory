/* jslint: devel:true */
var app = angular.module('addBiz');


app.controller('socialInfoCtrl', ['$scope', 'abDataFactory', function($scope, abDataFactory) {
  console.log('socialInfoCtrl LOADED');
  $scope.DF = abDataFactory;
  $scope.storage_array = $scope.DF.getData();

  $scope.biz = $scope.storage_array[0];

  if($scope.biz) {
    if($scope.biz.url) {
      console.log('UPDATING SOCIAL DATA-BINDINGS');
      $scope.biz.google_plus_url = $scope.biz.url; // google plus
    }
  }

}]);