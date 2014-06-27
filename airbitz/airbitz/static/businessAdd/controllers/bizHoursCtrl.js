/* jshint devel:true */
var app = angular.module('addBiz');


app.controller('bizHoursCtrl', ['$scope', 'abDataFactory', function ($scope, abDataFactory) {






  $scope.hours = {};
  $scope.hours.daysOfWeek = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat' ,'sun'];
  $scope.hours.selected = 'selectedHours';
  $scope.hours.options = [
      {'label': 'Open for Selected Hours', 'value': 'selectedHours'},
      {'label': 'Always Open', 'value': 'alwaysOpen'},
      {'label': 'Permanently Closed', 'value': 'permClosed'},
      {'label': 'No Hours Available', 'value': 'noneAvail'}
  ];

  $scope.hours.daysSelected = [];

  $scope.hours.businessHours = [
    {order: 0, day: 'mon', open: '', closed: ''},
    {order: 1, day: 'tue', open: '', closed: ''},
    {order: 2, day: 'wed', open: '', closed: ''},
    {order: 3, day: 'thu', open: '', closed: ''},
    {order: 4, day: 'fri', open: '', closed: ''},
    {order: 5, day: 'sat', open: '', closed: ''},
    {order: 6, day: 'sun', open: '', closed: ''}
  ];

  $scope.hours.selectDay = function (day) {
    var dayIndex = $scope.hours.daysSelected.indexOf(day);
    if ( dayIndex === -1 ) {
      $scope.hours.daysSelected.push(day);
      $scope.hours.updateHours();
    } else {
      $scope.hours.daysSelected.splice(dayIndex, 1);
    }
  };

  // this is an expression in the class {{ isDayActive(day) }}
  // and will return the class name that has a style to show that the day is active
  $scope.hours.isDayActive = function (day) {
    var dayIndex = $scope.hours.daysSelected.indexOf(day);
    var answer = dayIndex >= 0 ? 'active' : undefined;

    // console.log($scope.hours.daysSelected);
    // console.log(dayIndex + ' : ' + answer);

    return answer;
  };

  $scope.hours.selectDays = function (daysArray) {
    var alreadySelected = daysArray.toString() === $scope.hours.daysSelected.toString();

    if (alreadySelected) {
      $scope.hours.daysSelected = [];
    } else {
      $scope.hours.daysSelected = daysArray !== undefined ? daysArray : [];
    }

    $('.hours-open').focus();
    $scope.hours.updateHours();
  };

  $scope.hours.updateHours = function () {
    // clear errors
    $scope.hours.error = '';

    var daysSelected = $scope.hours.daysSelected;
    var hoursOpen = $scope.hours.hoursOpen;
    var hoursClosed = $scope.hours.hoursClosed;
    var businessHours = $scope.hours.businessHours;

    console.log('DAYS SELECTED : ' + daysSelected);

    if (daysSelected.length > 0) {


      // loop over days to add to table
      for (var i=0; i < daysSelected.length; i++) {
        var dayName = daysSelected[i];

        // console.log('DAY SELECTED: ' + i + ' of ' + daysSelected.length)
        // console.log('CHECKING: ' + dayName)

        // check if day is in businessHours array
        for (var j=0; j < businessHours.length ; j++) {
          if (businessHours[j].day === dayName) {

            // console.log('DUPLICATED SO REMOVING: ' + dayName)

            businessHours.splice(j, 1)

          } else {

            // console.log('DAY NOT IN LIST YET: ' + dayName)

          }
        }

        // object containing data to add to table
        var hoursRow = {
          'order': $scope.hours.daysOfWeek.indexOf(dayName),
          'day': dayName,
          'open': hoursOpen,
          'closed': hoursClosed
        };
        businessHours.push(hoursRow);
        $scope.hours.sortBusinessHours();

        // console.log('ADDING TO BUSINESHOURS: ' + JSON.stringify(hoursRow))

      }

      console.log('BUSINESSHOURS : ' + businessHours);
    } else {
      $scope.hours.error = 'To Update Select at Least 1 Day.';
    }


    if ($scope.hours.error) {
      // we had an error so user needs to fix data submitted
    } else {
      // clear form after adding
      /*
      $scope.hours.daysSelected = [];
      $scope.hours.hoursOpen = '';
      $scope.hours.hoursClosed = '';
      */
    }
  };

  $scope.hours.sortBusinessHours = function () {
    sortByKey($scope.hours.businessHours, 'order')
  };

  $scope.hours.clearDay = function(day) {
    console.log('CLICKED CLEAR: ' + day);
    var businessHours = $scope.hours.businessHours;

    for (var i=0; i < businessHours.length; i++) {
      if (i === day) {
        $scope.hours.businessHours[i].open = '';
        $scope.hours.businessHours[i].closed = '';
        console.log($scope.hours.businessHours[i]);
      }
    }
  };

  $scope.hours.loadFromCell = function (clicked) {
    console.log('CLICKED CELL : ' + clicked);
    var businessHours = $scope.hours.businessHours;
    for (var i=0; i < businessHours.length; i++) {
      if (i === clicked) {
        $scope.hours.hoursOpen = $scope.hours.businessHours[clicked].open ;
        $scope.hours.hoursClosed = $scope.hours.businessHours[clicked].closed;
        $scope.hours.selectDays([$scope.hours.businessHours[clicked].day]);
        console.log($scope.hours.businessHours[clicked]);
      }
    }
  };


}]);



// GENERAL UTILITY FUNCTIONS
function sortByKey(array, key) {
  var sorted = array.sort(function(a, b) {
      var x = a[key];
      var y = b[key];

      if (typeof x == "string")
      {
          x = x.toLowerCase();
          y = y.toLowerCase();
      }

      return ((x < y) ? -1 : ((x > y) ? 1 : 0));
  });
  console.log(sorted);
  return sorted;
}