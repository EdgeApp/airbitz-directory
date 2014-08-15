
// <select2 model="blah" />
var module = angular.module("select2", []);

module.directive('select2', ['$http', function($http) {
  return {
    restrict: 'A',
//    replace: true,
//    template: '<div class="asdfadsf"></div>',
    link: function(scope, element, attrs) {
        $http.get("/mgmt/api/cat/?page_size=2000").then(function(res){
          console.log(res.data);
          var d = $.map(res.data.results, function(m, i){
            console.log(arguments);
            return { id: m.id, text: m.name };
          });

          $(element).select2({
            width: '100%',
            multiple: true,
            data : d,
            createSearchChoice: function(term, data) {
                return { id: startId--, text: term };
            }
          }).on("change", function(e){
            scope.$apply(function(){
              scope.$parent[attrs.model] = e.val;
            });
          });

          window.ELEMENT = element;

        });
    }
  };
}]);