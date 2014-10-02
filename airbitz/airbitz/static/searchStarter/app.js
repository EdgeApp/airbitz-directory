/* jshint devel:true */

//console.log('LOADING...APP.JS');

var app = angular.module('searchStarter', [
    'ui.router',
    'ngAnimate'
]);

app.config(function($stateProvider, $urlRouterProvider, $httpProvider){
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';   //http://django-angular.readthedocs.org/en/latest/integration.html#xmlhttprequest

  $urlRouterProvider.otherwise('/');

  $stateProvider
    // route for home
      .state('home', {
        url: '/',
        templateUrl: '../partials/region-list.html',
        controller: 'abRegionList',
        resolve: {
          regionData: function($http){
            return $http.get('/mgmt/api/biz/countries').then(function(res){
              var results = res.data.results;
              return results;
            });
          }
        }
      })
      .state('region', {
        url: "/region/:region",
        templateUrl: "../partials/region.html",
        controller: 'abRegionDetails',
        resolve: {
          region: function($http, $stateParams){
            return $http.get('/mgmt/api/biz/country/' + $stateParams.region).then(function(res){
//              console.log('OUTPUT:');
//              console.log(res.data.results);
              return res.data.results;
            });
          }
        }
      })
});


app.controller('abRegionList', ['$scope', '$http', 'SimpleCache', 'regionData', function($scope, $http, SimpleCache, regionData) {
//  console.log('abRegionList CONTROLLER LOADED');
  $scope.regionData = regionData;
  $scope.bizCount = function() {
    var count = 0;
    for(var i=0; i < regionData.length; i++) {
      count += regionData[i].biz_count;
    }
    return count;
  }

  $scope.regionLookup = function(code) {
//    console.log('REGION LOOKUP ' + code);
    if(code === 'US') {
      return 'United States';
    }
  }

  $scope.regionClicked = function(region) {
    var $location = $('#input-location');
    var $search = $('#search-button');

    $location.val(region);

    $search.addClass('animated flash');
    $location.css({
      'border-color': '#2291cf',
      '-webkit-transition': 'border 100ms ease-out',
      '-moz-transition': 'border 100ms ease-out',
      '-o-transition': 'border 100ms ease-out'
    });

    setTimeout(function () {
      $search.removeClass('animated fadeInUp');
      $location.css({
        'border-color': '#ccc',
        '-webkit-transition': 'border 500ms ease-out',
        '-moz-transition': 'border 500ms ease-out',
        '-o-transition': 'border 500ms ease-out'
      });
    }, 2000);

    SimpleCache.put('country', region)
  }

}]);


app.controller('abRegionDetails', ['$scope', 'SimpleCache', 'region', function($scope, SimpleCache, region) {
//  console.log('abRegionDetails controller loaded');
  $scope.regionDetails = region;
  $scope.url_country_code = document.location.href.split('/')[document.location.href.split('/').length - 1];
  $scope.country = SimpleCache.get('country') || $scope.url_country_code;

  $('.searchStarter .loading-spinner').hide();

  $scope.bizCount = function() {
    var count = 0;
    for(var i=0; i < region.length; i++) {
      count += region[i].biz_count;
    }
    return count;
  };

  $scope.subRegionClicked = function(region, country){
    var $location = $('#input-location');
    var $term = $('#input-name-category');
    var $search = $('#search-button');

    $location.val(region + ', ' + country);
    $term.val('');

//    $search.addClass('animated fadeInUp');
    $location.css({
      'border-color': '#2291cf',
      '-webkit-transition': 'border 100ms ease-out',
      '-moz-transition': 'border 100ms ease-out',
      '-o-transition': 'border 100ms ease-out'
    });

    setTimeout(function(){
      $search.removeClass('animated flash');
      $location.css({
        'border-color': '#ccc',
        '-webkit-transition': 'border 500ms ease-out',
        '-moz-transition': 'border 500ms ease-out',
        '-o-transition': 'border 500ms ease-out'
      });
    }, 2000);

    $scope.showLoading();
    $search.click();

  };

  $scope.showLoading = function() {
    var $loadingSpinner = $('.searchStarter .loading-spinner');
    $loadingSpinner.show();
    $loadingSpinner.addClass('animated fadeInUp');
    $('.searchStarter .list-container').css('opacity', '.3');
  };

}]);

app.service('SimpleCache', ['$rootScope', function() {
  var cache = {};

  this.put = function(key, value) {
    cache[key] = value;
  };

  this.remove = function(key) {
    delete cache[key];
  };

  this.get = function(key) {
    return cache[key] || null;
  };

}]);