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

        $('.et_pb_slide_image').show();
        $appStoreLinks.css('visibility', 'visible');
        $appStoreLinks.addClass('slideInLeft');

        $iphoneSlider.css('visibility', 'visible');
        $iphoneSlider.addClass('animated bounceInDown');

    },1250);

    $('.ab-app-cta .app-install').hover(function(){
        $(this).find('.app-store').addClass('pulse infinite');
        $(this).find('.app-screenshot').addClass('pulse');
    }, function(){
        $(this).find('.app-store').removeClass('pulse infinite');
        $(this).find('.app-screenshot').removeClass('pulse');
    });

    $('#who-accepts-bitcoin').mouseenter(function() {
        $('#who-accepts-bitcoin').hide();
        $('#accepting-bitcoin').css('visibility', 'visible');
        $('#accepting-bitcoin').addClass('animated bounceInDown');
    });



});