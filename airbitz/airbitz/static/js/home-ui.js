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

  $("#see-app-in-action").jqueryVideoLightning({
    autoplay: 1,
    backdrop_opacity: .8
  });


  $('#app-demo-slides').carouFredSel({
    width: 212,
    height: 378,
    auto: {
      play: true
    },
    scroll: {
      pauseOnHover: true,
      fx: 'crossfade',
      duration: 1600,
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


$('.newsletter-signup').on('mouseover', function(){
  $('#email-signup-form').fadeIn();
  $(this).hide();
});



// EXMAPLE BUTTON SCROLL AND DRAW ATTENTION
//  $('#jump-who-accepts-bitcoin').on('click', function(){
//    showWhoAcceptsBitcoin();
//    $("html, body").animate({ scrollTop: 0 }, "slow");
//    $('#accepting-bitcoin').removeClass('animated bounceInDown pulse');
//    setTimeout(function() {
//      $('#accepting-bitcoin').addClass('animated pulse');
//    }, 750);
//    return false;
//  });

});
