/*jshint devel:true */
/* TODO: replace with modernizr */
function supports_html5_storage() {
  try {
    return 'localStorage' in window && window['localStorage'] !== null;
  } catch (e) {
    return false;
  }
}

function getMapMarkerContent(marker, m) {
    var html = 
      '<div class="map-marker-popup">' +
        '<div class="map-marker-image"><a href="' + m.url + '">' + m.img + '</a></div>' +
        '<div class="map-marker-info single-line">' +
          '<div class="map-marker-name">' + m.name + '</div>' +
          '<div class="map-marker-address">' + m.address + '</div>' +
          '<div class="map-marker-links"><a href="' + m.url + '">View Listing</a> | ' +
              '<a href="' + m.directions_url + '" target="_blank">Get Directions</a>' + 
          '</div>' +
        '</div>' +
        '<div class="map-marker-categories">' + m.cats + '</div>' +
      '</div>';
    return html;
}

(function() {
  var root = this;
  var AB = root.AB = {};

  AB.now = function() {
    return (new Date()).getTime();
  }
  AB.setNear = function() {
    var n = $('input.location').val() || '';
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
    if (false && supports_html5_storage()) {
      var loc = AB.getNear()
      if (loc) {
        $('input.location').val(loc);
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

      $.each(markers, function(i, m) {
        if (m.lat && m.lon) {
          var loc = new google.maps.LatLng(m.lat, m.lon);
          var marker = new google.maps.Marker({
              position: loc,
              map: map,
              title: m.name,
              animation: google.maps.Animation.DROP // TODO: ran out of time - https://developers.google.com/maps/documentation/javascript/examples/marker-animations-iteration
          });

          var ref = m;
          google.maps.event.addListener(marker, 'click', function(e) {
            infowindow.setContent(getMapMarkerContent(this, ref));
            infowindow.open(map, this);
          });

          google.maps.event.addListener(marker, 'mouseover', function(e) {
            infowindow.setContent(getMapMarkerContent(this, ref));
            infowindow.open(map, this);
          });

          bounds.extend(loc);
        }
      });
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
    var loc = $('input.location').val() || '';
    var engine = new Bloodhound({
      name: 'business',
      datumTokenizer: function(d) { return d; },
      queryTokenizer: Bloodhound.tokenizers.whitespace,
      minLength: 0,
      limit: 10,
      prefetch: {
        url: '/api/v1/category-suggest/?location=' + encodeURIComponent(loc),
        filter: function(data) {
          var m = $.map(data.results, function(e, i) {
              return { type: e.type, name: e.text, value: e.text };
          });
          return m;
        }
      },
      remote: {
        url: '/api/v1/autocomplete-business/?term=%QUERY',
        replace: function (url, uriEncodedQuery) {
          q = url.replace(/%QUERY/, uriEncodedQuery)
          if ($('input.location').val()) {
              q += "&location=" + encodeURIComponent(loc);
          }
          return q;
        },
        filter: function(data) {
          return $.map(data.results, function(e, i) {
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
      minLength: 0,
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
      var locFilter = function(data) {
        return data.results.map(function(s, i) {
            return { text: s, value: s };
        });
      };
      var engine = new Bloodhound({
        datumTokenizer: function(d) { return d; }, 
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        minLength: 0,
        prefetch: {
          url: '/api/v1/autocomplete-location/',
          filter: locFilter
        },
        remote: {
          url: '/api/v1/autocomplete-location/?term=%QUERY',
          filter: locFilter,
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
        $(this).val(datum.text);
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
