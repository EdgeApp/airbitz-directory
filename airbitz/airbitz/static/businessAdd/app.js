/* jshint devel:true */

var app = angular.module('addBiz', [
  'ui.router',
  'ngAnimate',
  'ngAutocomplete',
  'ui.bootstrap'
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
    .state('imageGather', {
      url: '/image-gather',
      templateUrl: '../partials/imageGather.html',
      controller: 'imageGatherCtrl'
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


    // all at once for admins
    .state('collectAll', {
      url: '/collect-all',
      views: {
        '': {
          templateUrl: '../partials/collectAllInfo.html',
          controller: 'collectAllInfo'
        },
        'generalInfo@collectAll': {
          templateUrl: '../partials/generalInfo.html',
          controller: 'generalInfoCtrl'
        },
        'locationInfo@collectAll': {
          templateUrl: '../partials/locationInfo.html',
          controller: 'locationInfoCtrl'
        },
        'socialInfo@collectAll': {
          templateUrl: '../partials/socialInfo.html',
          controller: 'socialInfoCtrl'
        },
        'geoInfo@collectAll': {
          templateUrl: '../partials/geoInfo.html',
          controller: 'geoInfoCtrl'
        },
        'bizHours@collectAll': {
          templateUrl: '../partials/bizHours.html',
          controller: 'bizHoursCtrl'
        },

      }
    })



    // other testing area
    .state('bizQuery', {
      url: '/biz-query',
      templateUrl: '../partials/bizQuery.html',
      controller: 'bizQueryCtrl'
    })

});












