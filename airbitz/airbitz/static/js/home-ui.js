/*jshint devel:true */

function afterEmailSubmission(resp){
    if (resp.result === 'success') {
        $('.inputEmail').val('');
        $('.inputText').val('');
    }
}


jQuery(function($) {

    $('#email-signup-form').ajaxChimp({
        url: 'https://airbitz.us3.list-manage.com/subscribe/post?u=af7e442f9bcaaff857bb5da03&amp;id=b7bd36890d',
        callback: afterEmailSubmission
    });

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


});