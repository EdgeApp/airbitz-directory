/*jshint devel:true */

function afterEmailSubmission(resp){
    if (resp.result === 'success') {
        $('#inputEmail').val('');
    }
}

jQuery(function($) {

    $('#email-signup-form').ajaxChimp({
        url: 'https://airbitz.us3.list-manage.com/subscribe/post?u=af7e442f9bcaaff857bb5da03&amp;id=b7bd36890d',
        callback: afterEmailSubmission
    });

    setTimeout(function(){
        $('.et_pb_slide_image').show();
    },1250);

    $('.marquee').marquee({
        pauseOnHover: true,
        //speed in milliseconds of the marquee
        duration: 8000,
        //gap in pixels between the tickers
        gap: 0,
        //time in milliseconds before the marquee will start animating
        delayBeforeStart: 0,
        //'left' or 'right'
        direction: 'left',
        //true or false - should the marquee be duplicated to show an effect of continues flow
        duplicated: true
    });

    $('.app-install').hover(function(){
        $(this).find('.app-store').addClass('animated pulse infinite');
        $(this).find('.app-screenshot').addClass('animated pulse');
    }, function(){
        $(this).find('.app-store').removeClass('animated pulse infinite');
        $(this).find('.app-screenshot').removeClass('animated pulse');
    });

});