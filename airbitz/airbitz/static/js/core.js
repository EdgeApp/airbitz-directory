/* TODO: replace with modernizr */
function supports_html5_storage() {
  try {
    return 'localStorage' in window && window['localStorage'] !== null;
  } catch (e) {
    return false;
  }
}

(function() {
  var root = this;
  var AB = root.AB = {};

  AB.now = function() {
    return (new Date()).getTime();
  }
  AB.setNear = function() {
    var n = $('#near').val();
    if (n) {
      localStorage.setItem("near", n);
      localStorage.setItem("nearDate", AB.now());
    }
  };
  AB.getNear = function() {
      var near = localStorage.getItem("near");
      var then = localStorage.getItem("nearDate");
      if (near && then && AB.now() - then < 1000 * 60) {
        return near;
      } else {
        return null;
      }
  };
  AB.setup = function() {
    if (supports_html5_storage()) {
      var near = AB.getNear()
      if (near) {
        $('#near').val(near);
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
  AB.addMap = function(selector, zoom, lat, lon, markers) {
    function initialize() {
      var mapOptions = {
        center: new google.maps.LatLng(lat, lon),
        zoom: zoom,
        disableDefaultUI: true,
        mapTypeId: google.maps.MapTypeId.ROADMAP
      };
      var bounds = new google.maps.LatLngBounds();
      var map = new google.maps.Map(selector[0], mapOptions);
      for (var i = 0; i < markers.length; ++i) {
        var m = markers[i];
        if (m.lat && m.lon) {
          var loc = new google.maps.LatLng(m.lat, m.lon);
          var marker = new google.maps.Marker({
              position: loc,
              map: map
          });
          bounds.extend(loc);
        }
      }
      map.fitBounds(bounds);
      map.panToBounds(bounds); 
    }
    google.maps.event.addDomListener(window, 'load', initialize);
    return map;
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
          if ($('#near').val()) {
              q += "&near=" + encodeURIComponent($('#near').val());
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
