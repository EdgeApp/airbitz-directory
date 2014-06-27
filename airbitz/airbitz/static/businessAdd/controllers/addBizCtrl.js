/* jshint devel:true */
var app = angular.module('addBiz');


app.controller('addBizCtrl', ['$scope', 'abDataFactory', function ($scope, abDataFactory) {
  $scope.DF = abDataFactory;
  $scope.storage_array = $scope.DF.getData();
  $scope.biz = {};

  $scope.query = {};
  $scope.query.bizId = 5;



  $scope.query.getBiz = function (bizId) {
    if(bizId) {
      abDataFactory.getBiz(bizId)
        .success(function (data) {
          $scope.DF.addData(data);
          console.log('getBiz: SUCCESS');
          $scope.makeUpdate('New Biz Data');
        })
        .error(function(status) {
          console.log('getBiz: ERROR');console.log(status);
        });
    }
  };

  // default query
  $scope.query.getBiz($scope.query.bizId);

  // trying to watch globally accessible data
  $scope.$watch('', function() {
    console.log('STORAGE_ARRAY CHANGED');
  });



  $scope.makeUpdate = function (text) {
    $scope.biz.updated = {};
    $scope.biz.updated.date = new Date();
    $scope.biz.updated.msg = text;
  };

  $scope.getGeolocation = function (data) {
    $scope.biz.geolocation = data;
  };

  $scope.loadForm = function () {
    $scope.msg = 'HERE IS THE MSG';
  };

}]);