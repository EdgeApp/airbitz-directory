/*jshint devel:true */

$(function() {

  if (bowser.android || bowser.ios) {

    if (bowser.ios) {
      $('.install-button').attr('href', 'https://itunes.apple.com/us/app/bitcoin-wallet-map-directory/id843536046?mt=8');
    }

    if (bowser.android) {
      $('.install-button').attr('href', 'https://play.google.com/store/apps/details?id=com.airbitz');
    }

    // utility function to increment a cookie counter by 1
    function hasBeenSeen(thing) {
      var count = $.cookie(thing, Number) || 0;
      var newCount = ++count;
      $.cookie(thing, newCount, {expires: 30});
    }

    // css adjustments and animation to show the bar
    function showMobileAppDownload() {
      $('#nav-mobile').css({
        'position': 'relative',
        'margin': '0'
      });
      $('body').css({
        'padding-top': '0'
      });
      $('.mobile-app-download').slideDown();
      hasBeenSeen('mobile-app-download');
    }

    // css adjustments and animation to hide the bar
    function hideMobileAppDownload() {
      $('.mobile-app-download').slideUp();
      $('#nav-mobile').css({
        'position': 'fixed'
      });

      $('body').css({
        'padding-top': '0'
      });
    }

    // each time we close we will increment the cookie via hasBeenSeen()
    $('.mobile-app-download .close').on('click', function () {
      hideMobileAppDownload();
      hasBeenSeen('mobile-app-download-hidden');
    });

    // only show app download screen if never seen or it has been closed 2x or less in the last 30 days
    if($.cookie('mobile-app-download-hidden') == undefined || $.cookie('mobile-app-download-hidden') < 2) {
      showMobileAppDownload();

      $(window).scroll(function (event) {
        var height = $(window).scrollTop();
        if(height > 64) {
          hideMobileAppDownload();
        }
        if(height < 65) {
          showMobileAppDownload();
        }
      });
    }

    if($('.mobile-app-download').is(':visible')) {

    }
  }

});