/*jshint devel:true */
/* TODO: replace with modernizr */
function supports_html5_storage() {
  try {
    return 'localStorage' in window && window['localStorage'] !== null;
  } catch (e) {
    return false;
  }
}

function getMapMarkerContent(marker, markerJSON) {
    for (var i = 0; i < markerJSON.length; i++ ) {
        var m = markerJSON[i];

        if (marker.getTitle() === m.name) {
            var html =  '<strong class="map-marker-name">' + m.name + '</strong><br />' +
                        m.cats + '<br />' +
                        '<a href="' + m.url + '">View Listing</a><br />' +
                        '<span>' + m.address + '</span>';
        }
    }
    return html;
}


(function() {
  var root = this;
  var AB = root.AB = {};

  AB.now = function() {
    return (new Date()).getTime();
  }
  AB.setNear = function() {
    var n = $('#location').val();
    if (n) {
      localStorage.setItem("location", n);
      localStorage.setItem("nearDate", AB.now());
    }
  };
  AB.getNear = function() {
      var loc = localStorage.getItem("location");
      var then = localStorage.getItem("nearDate");
      if (loc && then && AB.now() - then < 1000 * 60) {
        return loc;
      } else {
        return null;
      }
  };
  AB.setup = function() {
    if (supports_html5_storage()) {
      var loc = AB.getNear()
      if (loc) {
        $('#location').val(loc);
      }
    }
    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings) {
            if (!AB.Util.csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", $('meta[name="csrf-token"]').attr('content'));
            }
        }
    });
  };
  AB.addMap = function(selector, zoom, lat, lon, markers, polygon) {
    function initialize() {
      var mapOptions = {
        center: new google.maps.LatLng(lat, lon),
        zoom: zoom,
        disableDefaultUI: true,
        mapTypeId: google.maps.MapTypeId.ROADMAP
      };
      var bounds = new google.maps.LatLngBounds();
      var poly;
      var map = new google.maps.Map(selector[0], mapOptions);

      var infowindow = new google.maps.InfoWindow();

      for (var i = 0; i < markers.length; ++i) {
        var m = markers[i];

        if (m.lat && m.lon) {
          var loc = new google.maps.LatLng(m.lat, m.lon);
          var marker = new google.maps.Marker({
              position: loc,
              map: map,
              title: m.name,
              animation: google.maps.Animation.DROP // TODO: ran out of time - https://developers.google.com/maps/documentation/javascript/examples/marker-animations-iteration
          });

          google.maps.event.addListener(marker, 'click', function(e) {
            infowindow.setContent(getMapMarkerContent(this, markers));
            infowindow.open(map, this);
          });

          google.maps.event.addListener(marker, 'mouseover', function(e) {
            infowindow.setContent(getMapMarkerContent(this, markers));
            infowindow.open(map, this);
          });

          bounds.extend(loc);
        }
      }
      if (polygon) {
        var coords = [];
        for (var i = 0; i < polygon.length; ++i) {
          var m = polygon[i];
          if (m.lat && m.lon) {
            var loc = new google.maps.LatLng(m.lat, m.lon);
            coords.push(loc)
//            bounds.extend(loc);
          }
        }
        poly = new google.maps.Polygon({
          paths: coords,
          strokeColor: '#003399',
          strokeOpacity: 0.25,
          strokeWeight: 2,
          fillColor: '#336699',
          fillOpacity: 0.15
        });
        poly.setMap(map)
      }
      map.fitBounds(bounds);
      map.panToBounds(bounds); 
    }
    google.maps.event.addDomListener(window, 'load', initialize);
  };
  AB.addPlaceSearch = function(selector) {
    var engine = new Bloodhound({
      name: 'business',
      datumTokenizer: function(d) {
        return d.results; 
      },
      queryTokenizer: Bloodhound.tokenizers.whitespace,
      minLength: 0,
      remote: {
        url: '/api/v1/autocomplete-business/?term=%QUERY',
        replace: function (url, uriEncodedQuery) {
          q = url.replace(/%QUERY/, uriEncodedQuery)
          if ($('#location').val()) {
              q += "&location=" + encodeURIComponent($('#location').val());
          }
          return q;
        },
        filter: function(data) {
          return data.results.map(function(e, i) {
              return { type: e.type, name: e.text, value: e.text, id: e.bizId };
          });
        },
        rateLimitWait: 100
      }
    });
    engine.initialize();
    selector.typeahead({
      minLength: 0,
      hint: false,
      highlight: true
    }, {
      displaykey: 'name',
      name: 'business',
      source: engine.ttAdapter(),
      template: function(datum) {
          return '<p>' + datum.name + '</p>';
      }
    });
    selector.on('typeahead:selected', function (object, datum) {
      AB.setNear();
      if (datum.type === 'business' && datum.id) {
        location.href = '/biz/' + datum.id;
      }
    });
  };
  AB.addLocationSearch = function(selector, locSelector) {
      var values = ['On the Web', 'Current Location'];
      var defaultString = '';
      $.each(values, function(val) {
        return defaultString += val + ' ';
      });
      var local = new Bloodhound({
        datumTokenizer: function(d) { return defaultString.split(/\s+/); },
        queryTokenizer: function(d) { return defaultString.split(/\s+/); },
        local: $.map(values, function(val) {
          return { text: val, value: val };
        })
      });
      local.initialize();
      var engine = new Bloodhound({
        datumTokenizer: function(d) { return d.results; },
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        minLength: 0,
        remote: {
          url: '/api/v1/autocomplete-location/?term=%QUERY',
          filter: function(data) {
            return data.results.map(function(s, i) {
                return { text: s, value: s };
            });
          },
          rateLimitWait: 100
        }
      });
      engine.initialize();
      selector.typeahead({
        minLength: 0,
        hint: false,
        highlight: true
      }, [ {
        displaykey: 'text',
        name: 'always',
        source: local.ttAdapter(),
        templates: function(datum) {
          return datum.text;
        }
      }, {
        displaykey: 'text',
        name: 'location',
        source: engine.ttAdapter(),
        templates: function(datum) {
          return datum.text;
        }
      }]);
      selector.on('typeahead:selected', function (object, datum) {
        AB.setNear();
        $(this).val(data.text);
      });
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
