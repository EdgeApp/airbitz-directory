/*jshint devel:true */

var screen_lg = "screen and (min-width: 992px)";

function afterEmailSubmission(resp){
  if (resp.result === 'success') {
    $('.inputEmail').val('');
    $('.inputText').val('');
  }
}


jQuery(function($) {
  $('#email-signup-form').hide();

  $('#email-signup-form').on('click', function() {
    $.ajaxSetup({ crossDomain: true });
  });

  $('#email-signup-form').ajaxChimp({
    url: 'https://airbitz.us3.list-manage.com/subscribe/post?u=af7e442f9bcaaff857bb5da03&amp;id=b7bd36890d',
    callback: afterEmailSubmission
  });

  $('#app-demo-slides').mouseenter(function() {
    $('#see-app-in-action').css('visibility', 'visible');
    $('#see-app-in-action').removeClass('animated fadeOut');
    $('#see-app-in-action').addClass('animated fadeIn');
  });


  // home page lightbox video
  $('.iphone-app-slider .video').magnificPopup({type: 'iframe'});
  $('.container .video').magnificPopup({type: 'iframe'});


  var appDemoSliderWidth = 260;
  var appDemoSliderHeight = 360;

  // adjust size for larger screens
  enquire.register(screen_lg, function() {
    appDemoSliderWidth = 406;
    appDemoSliderHeight = 560;
  });

  $('#app-demo-slides').carouFredSel({
    width: appDemoSliderWidth,
    height: appDemoSliderHeight,
    auto: {
      play: true
    },
    scroll: {
      pauseOnHover: true,
      fx: 'crossfade',
      duration: 1500,
      onBefore: function() {
        $('#see-app-in-action').css('visibility', 'hidden');
        $('#see-app-in-action').removeClass('animated fadeIn');
        $('#see-app-in-action').addClass('animated fadeOut');
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
      '-0-transition': 'all .25s'
    });
  }, function(){
    $(this).find('.app-store').css({
      'zoom': '100%'
    });
  });


  setTimeout(function(){
    $('.newsletter-signup').hide();
    $('#email-signup-form').fadeIn();
  }, 5000);

  // hide particles after 5 min
  setTimeout(function(){
    $('#landing-particles').hide();
  }, 300000);

  // on resize hide
  $(window).resize(function(){
    $('#landing-particles').hide();
  });


if(!bowser.android && !bowser.ios ) {
  /* config dom id (optional) + config particles params */
  particlesJS('landing-particles', {
    particles: {
      color: '#fff',
      shape: 'circle', // "circle", "edge" or "triangle"
      opacity:.4,
      size: 5,
      size_random: true,
      nb: 150,
      line_linked: {
        enable_auto: true,
        distance: 360,
        color: '#fff',
        opacity:.2,
        width: 2,
        condensed_mode: {
          enable: false,
          rotateX: 600,
          rotateY: 600
        }
      },
      anim: {
        enable: true,
        speed: 1.25
      }
    },
    interactivity: {
      enable: true,
      mouse: {
        distance: 300
      },
      detect_on: 'canvas', // "canvas" or "window"
      mode: 'grab',
      line_linked: {
        opacity: .6
      },
      events: {
        onclick: {
          enable: false,
          mode: 'push', // "push" or "remove"
          nb: 4
        }
      }
    },
    /* Retina Display Support */
    retina_detect: true
  });
}



// BUTTON SCROLL AND DRAW ATTENTION
//  $('#learn-more-wallet').on('click', function(){
//    $("html, body").animate({ scrollTop: $('#features-wallet').offset().top - 65 }, "slow");
//  });
//  $('#learn-more-directory').on('click', function(){
//    $("html, body").animate({ scrollTop: $('#features-directory').offset().top - 65 }, "slow");
//  });

});
