/* jshint devel:true */
var app = angular.module('addBiz');


var abDataFactory = function ($http, $q) {
  var factory = {};

  // fetches business data from a business id
  factory.getBiz = function(bizId) {
    var deferred = $q.defer();
    var http_config = {
      url: 'http://127.0.0.1:8000/mgmt/api/biz/' + bizId,
      method: 'GET'
    };

    $http(http_config).success(function (data) {
      console.log('getBiz SUCCESS');
      deferred.resolve(data);
    }).error(function(){
      console.log('getBiz FAILED');
      deferred.reject();
    });

    return deferred.promise;
  };

  return factory;
};

app.factory('abDataFactory', abDataFactory);