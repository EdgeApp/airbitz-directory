/* jshint devel:true */
var app = angular.module('addBiz');


app.filter('titleCase', function() {
  return function(str) {
    return (str == undefined || str === null) ? '' : str.replace(/_|-/, ' ').replace(/\w\S*/g, function(txt){
      return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
  }
});