(function() {
  var root = this;
  var AB = root.AB = {};

  AB.setup = function() {
    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings) {
            if (!AB.Util.csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", $('meta[name="csrf-token"]').attr('content'));
            }
        }
    });
  };

  AB.addMap = function(selector, zoom, lat, lon, markers) {
      function initialize() {
          var mapOptions = {
              center: new google.maps.LatLng(lat, lon),
              zoom: zoom,
              disableDefaultUI: true,
              mapTypeId: google.maps.MapTypeId.ROADMAP
          };
          var map = new google.maps.Map(selector[0], mapOptions);
          for (var i = 0; i < markers.length; ++i) {
              var m = markers[i];
              var marker = new google.maps.Marker({
                  position: new google.maps.LatLng(m.lat, m.lon),
                  map: map
              });
          }
      }
      google.maps.event.addDomListener(window, 'load', initialize);
      return map;
  };
  AB.addPlaceSearch = function(selector) {
      var end = '';
      var geo = Geo.latestLocation();
      if (geo) {
          end += '&ll=' + geo.coords.latitude + ',' + geo.coords.longitude;
      }
      selector.typeahead([{
          name: 'business',
          remote: {
              url: '/api/v1/autocomplete-business/?term=%QUERY' + end,
              replace: function (url, uriEncodedQuery) {
                  q = url.replace(/%QUERY/, uriEncodedQuery)
                  if ($('#near').val()) {
                      q += "&location=" + encodeURIComponent($('#near').val());
                  }
                  return q;
              },
              filter: function(data) {
                  return data.results.map(function(e, i) {
                      return { type: e.type, name: e.text, value: e.text, id: e.bizId };
                  });
              }
          },
          template: function(datum) {
              return '<p>' + datum.name + '</p>';
          }
      }]);
      selector.on('typeahead:selected', function (object, datum) {
          if (datum.type === 'business' && datum.id) {
            location.href = '/biz/' + datum.id;
          } else {
            location.href = '/search?category=' + encodeURIComponent(datum.value) + 
                                   '&location=' + encodeURIComponent($('#near').val());
          }
      });
  };
  AB.addLocationSearch = function(selector, locSelector) {
      var end = '';
      var geo = Geo.latestLocation();
      if (geo) {
          end += '&lat=' + geo.coords.latitude + '&lon=' + geo.coords.longitude;
      }
      selector.typeahead([{
          name: 'location',
          remote: {
              url: '/api/v1/autocomplete-location/?term=%QUERY' + end,
              filter: function(data) {
                  return data.results.map(function(s, i) {
                      return { text: s, value: s };
                  });
              }
          },
          rateLimitWait: 0,
          template: function(datum) {
              return '<p>' + datum.text + '</p>';
          }
      }]);
      selector.on('typeahead:selected', function (object, datum) {
          $(this).val(data.text);
      });
  };
  var Geo = AB.Geo = {
      latestLocation: function() {
          var cookie = Util.getCookie('geo');
          try {
              var geo = JSON.parse(cookie);
          } catch (e) {
              console.log(e);
          }
          return geo;
      },
      requestLocation: function() {
          var now = new Date();
          var geo = this.latestLocation();
          if (geo) {
              try {
                  var then = new Date(geo.timestamp).getTime();
                  if (now - then < 1000 * 60 * 60 * 1) {
                      return;
                  }
              } catch (e) {
                  console.log(e);
              }
          }
          if (navigator.geolocation) {
              navigator.geolocation.getCurrentPosition(this.postPosition);
          }
      },
      postPosition: function(geo) {
          Util.setCookie('geo', JSON.stringify(geo), 1);
      }
  };
  var Util = AB.Util = {
      csrfSafeMethod: function(method) {
          return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
      },
      setCookie: function(c_name, value, exdays) {
          var exdate = new Date();
          exdate.setDate(exdate.getDate() + exdays);
          var c_value = escape(value) + ((exdays===null) ? "" : "; expires="+exdate.toUTCString());
          document.cookie=c_name + "=" + c_value;
      },
      getCookie: function(c_name) {
          var c_value = document.cookie;
          var c_start = c_value.indexOf(" " + c_name + "=");
          if (c_start == -1) {
              c_start = c_value.indexOf(c_name + "=");
          }
          if (c_start == -1) {
              c_value = null;
          } else {
              c_start = c_value.indexOf("=", c_start) + 1;
              var c_end = c_value.indexOf(";", c_start);
              if (c_end == -1) {
              c_end = c_value.length;
              }
              c_value = unescape(c_value.substring(c_start,c_end));
          }
          return c_value;
      }
  };
}).call(this);
