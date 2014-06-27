/* jshint devel:true */
var app = angular.module('addBiz');


app.filter('titleCase', function() {
  return function(str) {
    return (str == undefined || str === null) ? '' : str.replace(/_|-/, ' ').replace(/\w\S*/g, function(txt){
      return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
  }
});

app.filter('truncate', function () {
  return function (text, length, end) {
    if (isNaN(length))
      length = 10;
    if (end === undefined)
      end = "...";
    if (text.length <= length || text.length - end.length <= length) {
      return text;
    }
    else {
      return String(text).substring(0, length - end.length) + end;
    }
  };
});