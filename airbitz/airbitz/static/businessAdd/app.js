/* jshint devel:true */

var app = angular.module('addBiz', [
    'ui.router'
]);

app.config(function($stateProvider, $urlRouterProvider, $httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';   //http://django-angular.readthedocs.org/en/latest/integration.html#xmlhttprequest

    $urlRouterProvider.otherwise('');

    $stateProvider
        // route for home
        .state('home', {
            url: '/',
            templateUrl: '../partials/placeLookup.html',
            controller: 'addBizCtrl',
        })
        .state('collectInfo', {
            url: 'collect-info',
            templateUrl: '../partials/collectInfo.html',
            controller: function ($scope) {
                $scope.msg = 'How is this?';
            },
        })
        .state('collectInfo.bizHours', {
            url: 'biz-hours',
            templateUrl: '../partials/bizHours.html',
            controller: 'bizHoursCtrl'
        })
});






