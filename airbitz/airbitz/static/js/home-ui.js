/*jshint devel:true */

function afterEmailSubmission(resp){
    if (resp.result === 'success') {
        $('.inputEmail').val('');
    }
}

function showRegionSignup() {
    $('#general-signup').hide();
    $('#area-form').removeClass('fadeOut').addClass('animated fadeIn').show();
}

function hideGeneralSignup() {
    $('#general-signup').removeClass('fadeOut').addClass('animated fadeIn').show();
}


jQuery(function($) {

    $('#email-signup-form').ajaxChimp({
        url: 'https://airbitz.us3.list-manage.com/subscribe/post?u=af7e442f9bcaaff857bb5da03&amp;id=b7bd36890d',
        callback: afterEmailSubmission
    });

    var $regionSignupForm = $('#region-signup-form');
    if($regionSignupForm) {
        $regionSignupForm.ajaxChimp({
            url: 'https://airbitz.us3.list-manage.com/subscribe/post?u=af7e442f9bcaaff857bb5da03&amp;id=b7bd36890d',
            callback: afterEmailSubmission
        });
    }

    setTimeout(function(){
        $('.et_pb_slide_image').show();
        $('#general-signup .app-install').addClass('animated slideInRight');
    },1250);

    $('.ab-app-cta .app-install').hover(function(){
        $(this).find('.app-store').addClass('animated pulse infinite');
        $(this).find('.app-screenshot').addClass('animated pulse');
    }, function(){
        $(this).find('.app-store').removeClass('animated pulse infinite');
        $(this).find('.app-screenshot').removeClass('animated pulse');
    });


    $('#cancelEmail').on('click', function(e){
        e.preventDefault();
        hideGeneralSignup();
        $('#area-form').hide();
    });

    $('#cancelOther').on('click', function(e){
        e.preventDefault();
        hideGeneralSignup();
        $('.region-tabs a:first').tab('show');
    });

    $('#region-other-area-form').on('click', function(){
        $('#general-signup').hide();
        $('#area-form').addClass('animated fadeOut').hide();
    });

});