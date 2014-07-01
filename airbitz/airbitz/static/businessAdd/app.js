/* jshint devel:true */

var app = angular.module('addBiz', [
  'ui.router',
  'ngAnimate',
  'ngAutocomplete'
]);

app.config(function($stateProvider, $urlRouterProvider, $httpProvider) {
  $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';   //http://django-angular.readthedocs.org/en/latest/integration.html#xmlhttprequest

  $urlRouterProvider.otherwise('/');

  $stateProvider
    // route for home
    .state('placeLookup', {
      url: '/',
      templateUrl: '../partials/placeLookup.html',
      controller: 'addBizCtrl'
    })
    .state('collectInfo', {
      url: '/collect-info',
      templateUrl: '../partials/collectInfo.html'
    })
    .state('generalInfo', {
      url: '/general-info',
      templateUrl: '../partials/generalInfo.html',
      controller: 'generalInfoCtrl'
    })
    .state('locationInfo', {
      url: '/location-info',
      templateUrl: '../partials/locationInfo.html',
      controller: 'locationInfoCtrl'
    })
    .state('geoInfo', {
      url: '/geo-info',
      templateUrl: '../partials/geoInfo.html',
      controller: 'geoInfoCtrl'
    })
    .state('socialInfo', {
      url: '/social-info',
      templateUrl: '../partials/socialInfo.html',
      controller: 'socialInfoCtrl'
    })
    .state('bizHours', {
      url: '/biz-hours',
      templateUrl: '../partials/bizHours.html',
      controller: 'bizHoursCtrl'
    })
    .state('imageGatherer', {
      url: '/image-gather',
      templateUrl: '../partials/imageGather.html',
      controller: function() {
        console.log('imageGatherCtrl LOADED')
      }
    })
    .state('bizPreview', {
      url: '/biz-preview',
      templateUrl: '../partials/bizPreview.html',
      controller: function() {
        console.log('bizPreviewCtrl LOADED')
      }
    })
    .state('finishedThankYou', {
      url: '/thank-you',
      templateUrl: '../partials/finishedThankYou.html',
      controller: function() {
        console.log('finishedThankYouCtrl LOADED')
      }
    })


    // other testing area
    .state('bizQuery', {
      url: '/biz-query',
      templateUrl: '../partials/bizQuery.html',
      controller: 'bizQueryCtrl'
    })

});












