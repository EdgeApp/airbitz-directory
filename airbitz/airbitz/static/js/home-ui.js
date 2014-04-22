/*jshint devel:true */

function afterEmailSubmission(resp){
    if (resp.result === 'success') {
        $('.inputEmail').val('');
    }
}

function showRegionSignup() {
    $('#general-signup').hide();
    $('#area-form').removeClass('fadeOut').addClass('fadeIn').show();
}

function showGeneralSignup() {
    $('#general-signup').removeClass('fadeOut').addClass('fadeIn').show();
}

function hideGeneralSignup() {
    $('#general-signup').removeClass('fadeIn').addClass('fadeOut').hide();
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
        $('#general-signup .app-install').addClass('slideInRight');
    },1250);

    $('.ab-app-cta .app-install').hover(function(){
        $(this).find('.app-store').addClass('pulse infinite');
        $(this).find('.app-screenshot').addClass('pulse');
    }, function(){
        $(this).find('.app-store').removeClass('pulse infinite');
        $(this).find('.app-screenshot').removeClass('pulse');
    });


    $('#cancelEmail').on('click', function(e){
        e.preventDefault();
        showGeneralSignup();
        $('#area-form').hide();
    });

    $('#cancelOther').on('click', function(e){
        e.preventDefault();
        showGeneralSignup();
        $('.region-tabs a:first').tab('show');
    });

    $('#button-region-other').on('click', function(){
        hideGeneralSignup();
        $('#area-form').addClass('fadeOut').hide();
    });

    $('.region-tabs .tab-button:not(#button-region-other)').on('click', function(){
        showGeneralSignup();
        $('#area-form').addClass('fadeOut').hide();
        console.log('SHOW GENERAL')
    });



});