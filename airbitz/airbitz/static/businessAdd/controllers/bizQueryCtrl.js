/* jshint devel:true */
var app = angular.module('addBiz');


app.controller('bizQueryCtrl', ['$scope', 'abDataFactory', function($scope, abDataFactory) {
  console.log('bizQuery LOADED');

  $scope.DF = abDataFactory;

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
//  $scope.query.getBiz($scope.query.bizId);


  $scope.makeUpdate = function (text) {
    $scope.biz.updated = {};
    $scope.biz.updated.date = new Date();
    $scope.biz.updated.msg = text;
  };


}]);