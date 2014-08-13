/* jshint devel:true */

console.log('LOADING...APP.JS');

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
            return $http.get('http://127.0.0.1:8000/mgmt/api/biz/country/' + $stateParams.region).then(function(res){
              console.log('OUTPUT:');
              console.log(res.data.results);
              return res.data.results;
            });
          }
        }
      })
});


app.controller('abRegionList', ['$scope', '$http', 'regionData', function($scope, $http, regionData) {
  console.log('abRegionList CONTROLLER LOADED');
  $scope.regionData = regionData;
  $scope.regionLookup = function(code) {
    console.log('REGION LOOKUP ' + code);
    if(code === 'US') {
      return 'United States';
    }
  }

}]);


app.controller('abRegionDetails', ['$scope', 'region', function($scope, region) {
  console.log('abRegionDetails controller loaded');
  $scope.regionDetails = region;

  $scope.subRegionClicked = function(region, country){
    var $location = $('#input-location');
    var $search = $('#search-button');

    $location.val(region + ', ' + country);

    $search.addClass('animated fadeInUp');
    $location.css({
      'border-color': '#2291cf',
      '-webkit-transition': 'border 100ms ease-out',
      '-moz-transition': 'border 100ms ease-out',
      '-o-transition': 'border 100ms ease-out'
    });

    setTimeout(function(){
      $search.removeClass('animated fadeInUp');
      $location.css({
        'border-color': '#ccc',
        '-webkit-transition': 'border 500ms ease-out',
        '-moz-transition': 'border 500ms ease-out',
        '-o-transition': 'border 500ms ease-out'
      });
    }, 1000);

  };


}]);