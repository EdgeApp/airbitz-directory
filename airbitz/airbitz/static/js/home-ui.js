/*jshint devel:true */

function afterEmailSubmission(resp){
    if (resp.result === 'success') {
        $('.inputEmail').val('');
        $('.inputText').val('');
    }
}


jQuery(function($) {
    $('#email-signup-form').on('click', function() {
        $.ajaxSetup({ crossDomain: true });
    });
    
    $('#email-signup-form').ajaxChimp({
        url: 'https://airbitz.us3.list-manage.com/subscribe/post?u=af7e442f9bcaaff857bb5da03&amp;id=b7bd36890d',
        callback: afterEmailSubmission
    });

    $('#app-demo-slides').mouseenter(function() {
        $('#see-app-in-action').css('visibility', 'visible');
        $('#see-app-in-action').addClass('bounceInDown');
    });

    $("#see-app-in-action").jqueryVideoLightning({
        autoplay: 1,
        backdrop_opacity: .8
    });


    $('#app-demo-slides').carouFredSel({
      width: 238,
      height: 360,
      auto: {
        play: true
      },
      scroll: {
        pauseOnHover: true,
        fx: 'crossfade',
        duration: 800,
        onBefore: function() {
          $('#see-app-in-action').css('visibility', 'hidden');
          $('#see-app-in-action').removeClass('pulse');
        }
      }
    });

    setTimeout(function(){
        var $appStoreLinks = $('#app-store-links');
        var $iphoneSlider = $('.iphone-slider');

        $('.landing-module').backstretch('resize');

        $('.et_pb_slide_image').show();
        $appStoreLinks.css('visibility', 'visible');
        $appStoreLinks.addClass('slideInLeft');

        $iphoneSlider.css('visibility', 'visible');
        $iphoneSlider.addClass('animated bounceInDown');

    },1250);

    $('.ab-app-cta .app-install').hover(function(){
        $(this).find('.app-store').css({
            'zoom': '110%',
            'transition': 'all .25s',
            '-webkit-transition': 'all .25s',
            '-moz-transition': 'all .25s',
            '-0-transition': 'all .25s',
        });
    }, function(){
        $(this).find('.app-store').css({
          'zoom': '100%',
        });
    });

    if($.cookie('accepting-bitcoin', Number) > 1) {
      showWhoAcceptsBitcoin();
    } else{
      $('#who-accepts-bitcoin').css('visibility', 'visible');
      $('#reveal-who-accepts-bitcoin').mouseenter(function() {
          showWhoAcceptsBitcoin();
      });
    }

    function showWhoAcceptsBitcoin() {
      $('#who-accepts-bitcoin').hide();
      $('#accepting-bitcoin').css('visibility', 'visible');
      $('#accepting-bitcoin').addClass('animated bounceInDown');
      hasBeenSeen('accepting-bitcoin', 1);
    }

    function hasBeenSeen(thing, expiration) {
      var count = $.cookie(thing, Number) || 0;
      var newCount = ++count;
      $.cookie(thing, newCount, {expires: expiration});
    }

    $('#jump-who-accepts-bitcoin').on('click', function(){
      showWhoAcceptsBitcoin();
      $("html, body").animate({ scrollTop: 0 }, "slow");
      $('#accepting-bitcoin').removeClass('animated bounceInDown pulse');
      setTimeout(function() {
        $('#accepting-bitcoin').addClass('animated pulse');
      }, 750);
      return false;
    });


    // display navbar after first scroll and hide if all the way at top
    $(window).scroll(function() {
      var y = $(window).scrollTop();

      if (y > 50) {
        console.log('show');
        $('#nav-desktop').css({'visibility': 'visible'});
      } else {
        $('#nav-desktop').css({'visibility': 'hidden'});
      }
    });

});