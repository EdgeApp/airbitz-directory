/* jshint devel:true */
var app = angular.module('addBiz');


var abDataFactory = function ($http, $q) {
  var factory = {};
  var storage_array = [];
  var http_config = {};



  factory.appendData = function (data) {
    console.log('appendData:');console.log(data);
    if(data !== undefined) {
      storage_array.push(data);
    }
  };


  factory.updateData = function (data) {
    console.log('updateData UPDATING:');console.log(data);
    if(data !== undefined) {
      if(storage_array.length) {
        factory.removeData(0);
      }
      storage_array.push(data);
    }
  };


  factory.removeData = function(id) {
    var index;
    // checking for item in array
    for(var i=0; i<storage_array.length; i++) {
      if(id === storage_array[i].id){
        console.log('removeData FOUND ' + storage_array[id]);
        index = i;
      }
    }
    console.log('removeData REMOVING: '); console.log(storage_array[id]);
    storage_array.splice(index, 1);
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