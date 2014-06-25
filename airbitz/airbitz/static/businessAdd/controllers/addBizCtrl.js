/* jshint devel:true */
var app = angular.module('addBiz');


app.controller('addBizCtrl', ['$scope', function ($scope) {
  $scope.updated = 'Waiting for updates...';

  $scope.makeUpdate = function (text) {
    if(!text) {
      $scope.updated = new Date();
    }
  };

  $scope.loadForm = function () {
    $scope.msg = 'HERE IS THE MSG';
  };

  $scope.getGeolocation = function (data) {
    $scope.geolocation = data;
  }
}]);