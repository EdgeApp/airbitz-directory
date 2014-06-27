/* jshint devel:true */
var app = angular.module('addBiz');


var abDataFactory = function ($http, $q) {
  var factory = {};
  var storage_array = [];
  var http_config = {};



  factory.addData = function (data) {
    console.log('addData:');console.log(data);
    storage_array.push(data);
  };



  factory.getData = function () {
    return storage_array;
  };



  // fetches business data from a business id
  factory.getBiz = function(bizId) {
    var deferred = $q.defer();

    http_config.url = 'http://127.0.0.1:8000/mgmt/api/biz/' + bizId;
    http_config.method = 'GET';

    return $http(http_config);
  };



  return factory;
};

app.factory('abDataFactory', abDataFactory);