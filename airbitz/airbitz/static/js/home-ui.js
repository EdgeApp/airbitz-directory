/*jshint devel:true */

jQuery(function($) {

    $('#email-signup-form').ajaxChimp({
        url: 'https://airbitz.us3.list-manage.com/subscribe/post?u=af7e442f9bcaaff857bb5da03&amp;id=b7bd36890d'
    });


    setTimeout(function(){
        $('.et_pb_slide_image').show();
    },1250);

});