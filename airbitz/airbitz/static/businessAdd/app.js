/* jshint devel:true */

var app = angular.module('addBizApp', [
    'ui.router'
]);

app.config(function($stateProvider, $urlRouterProvider, $httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';   //http://django-angular.readthedocs.org/en/latest/integration.html#xmlhttprequest

    $urlRouterProvider.otherwise('/');

    $stateProvider
        // route for home
        .state('home', {
            url: '/',
            controller: 'addBizCtrl',
        })
        .state('collectInfo', {
            url: 'collect-info',
            templateUrl: 'partials/collectInfo.html',
            controller: function ($scope) {
                $scope.msg = 'How is this?';
            },
        })
});


app.controller('addBizCtrl', ['$scope', function ($scope) {
    $scope.updated = 'Waiting for updates...';

    $scope.makeUpdate = function (text) {
        if(!text) {
            $scope.updated = new Date();
        }
    };

    $scope.loadForm = function() {
        $scope.msg = 'HERE IS THE MSG';
    };

    $scope.getGeolocation = function (data) {
        $scope.geolocation = data;
    }
  }]);