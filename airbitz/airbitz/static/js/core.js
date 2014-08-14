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

  AB.geoTimeout = 1000 * 60 * 60 * 1;
  AB.now = function() {
    return (new Date()).getTime();
  }
  AB.setLL = function() {
    var geo = AB.Geo.latestLocation();
    var $ll = $('#ll');
    if (geo && geo.coords) {
      var ll = geo.coords.latitude + ',' + geo.coords.longitude;
      if ($ll.length) {
        $ll.val(ll);
      } else {
        $('<input>')
          .attr('type','hidden')
          .attr('name', 'll')
          .attr('id', 'll')
          .attr('value', ll)
          .appendTo('#navbar-search');
      }
    } else {
      $ll.remove();
    }
  };
  AB.setNear = function() {
    if (AB.Geo.latestLocation()) {
      AB.setLL();
    } else {
      AB.Geo.requestLocation(function(geo) {
        AB.setLL();
        $.getJSON('/api/v1/location-suggest/?ll=' + ll).done(function(data) {
          if (data && data.near) {
            $('input.location').val(data.near);
          }
        });
      });
    }
  };
  AB.setup = function() {
    AB.setNear();

    $.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings) {
            if (!AB.Util.csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", $('meta[name="csrf-token"]').attr('content'));
            }
            xhr.setRequestHeader("Authorization", "Token 0ccff150ed4633136f04eab2d8454d928e6ff584");
        }
    });
  };
  AB.addMap = function(selector, zoom, lat, lon, markers, polygon) {
    function initialize() {
      var mapOptions = {
        center: new google.maps.LatLng(lat, lon),
        zoom: zoom,
        maxZoom: 16,
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
      if (markers && markers.length > 1) {
        map.fitBounds(bounds);
        map.panToBounds(bounds); 
      }
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
        url: '/api/v1/autocomplete-business/?location=' + encodeURIComponent(loc),
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
      if (datum.type === 'business' && datum.id) {
        location.href = '/biz/' + datum.id;
      }
    });
    selector.click(function() {
      $(this).select();
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
      var updatePlace = function() {
        $('input.term').typeahead('destroy');
        AB.addPlaceSearch($('input.term'));
      };
      selector.on('typeahead:selected', function (object, datum) {
        $(this).val(datum.text);
        updatePlace();
      });
      selector.click(function() {
        $(this).select();
      });
      selector.change(updatePlace);
      selector.blur(updatePlace);
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
    requestLocation: function(cb) {
      var now = new Date();
      var geo = this.latestLocation();
      if (geo) {
        try {
            var then = new Date(geo.timestamp).getTime();
            if (now - then < AB.geoTimeout) {
                return;
            }   
        } catch (e) {
            console.log(e);
        }   
      }   
      var that = this;
      var now = AB.now();
      var then = AB.Util.getCookie('geo_timestamp');
      if (navigator.geolocation 
          && (then == null || now - then > AB.geoTimeout)) {
        var options = {
          enableHighAccuracy: true,
          timeout: 5000,
          maximumAge: 0
        };
        AB.Util.setCookie('geo_timestamp', AB.now(), 1); 
        navigator.geolocation.getCurrentPosition(function(geo) {
          that.postPosition(geo, cb);
        }, function(err) { }, options);
      }   
    },  
    postPosition: function(geo, cb) {
      Util.setCookie('geo', JSON.stringify(geo), 1); 
      cb(geo);
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
