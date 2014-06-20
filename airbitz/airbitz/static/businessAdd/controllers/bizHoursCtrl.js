/* jshint devel:true */
var app = angular.module('addBiz');


app.controller('bizHoursCtrl', ['$scope', function ($scope) {
  $scope.daysOfWeek = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat' ,'sun'];

  $scope.hours = {}
  $scope.hours.selected = 'selectedHours';
  $scope.hours.options = [
      {'label': 'Open for Selected Hours', 'value': 'selectedHours'},
      {'label': 'Always Open', 'value': 'alwaysOpen'},
      {'label': 'Permanently Closed', 'value': 'permClosed'},
      {'label': 'No Hours Available', 'value': 'noneAvail'},
  ];

  $scope.hours.daysSelected = [];

  $scope.hours.selectDay = function (day) {
    var dayIndex = $scope.hours.daysSelected.indexOf(day);
    if ( dayIndex === -1 ) {
      $scope.hours.daysSelected.push(day);
    } else {
      var removed = $scope.hours.daysSelected.splice(dayIndex, 1);
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
    $scope.hours.daysSelected = daysArray !== undefined ? daysArray : [];
  };


  $scope.hours.businessHours = [];

  $scope.hours.addHours = function (daysSelected, hoursOpen, hoursClosed) {
    var businessHours = $scope.hours.businessHours;

    // console.log(daysSelected)

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
        'day': dayName,
        'open': hoursOpen,
        'closed': hoursClosed
      };
      businessHours.push(hoursRow);

      // console.log('ADDING TO BUSINESHOURS: ' + JSON.stringify(hoursRow))

    }

    console.log($scope.hours.businessHours);

    if ($scope.hours.error) {
      // we had an error so user needs to fix data submitted
    } else {
      // clear form after adding
      $scope.hours.daysSelected = [];
      $scope.hours.hoursOpen = '';
      $scope.hours.hoursClosed = '';
    }
  }


}]);