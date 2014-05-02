/*jshint devel:true */

function scrollTop() {
    $("html, body").animate({ scrollTop: 0 }, "slow");
}

function afterEmailSubmission(resp){
    if (resp.result === 'success') {
        $('.inputEmail').val('');
    }
}

function showRegionSignup() {
    $('#general-signup').removeClass('fadeIn').addClass('fadeOut').hide();
    $('.area-list').removeClass('fadeIn').addClass('fadeOut').hide();
    $('#area-form').removeClass('fadeOut').addClass('fadeIn tada').show();
    scrollTop();
}

function showGeneralSignup() {
    $('#general-signup').removeClass('fadeOut').addClass('fadeIn').show();
    $('.area-list').removeClass('fadeOut').addClass('fadeIn').show();
    scrollTop();
}

function hideGeneralSignup() {
    $('#general-signup').removeClass('fadeIn').addClass('fadeOut').hide();
    $('.area-list').removeClass('fadeIn').addClass('fadeOut').hide();
    scrollTop();
}


jQuery(function($) {

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
    });


    var $regionSignupForm = $('#region-signup-form');
    if($regionSignupForm) {
        $regionSignupForm.ajaxChimp({
            url: 'https://airbitz.us3.list-manage.com/subscribe/post?u=af7e442f9bcaaff857bb5da03&amp;id=b7bd36890d',
            callback: afterEmailSubmission
        });
    }
    var $regionSignupFormOther = $('#region-signup-form-other');
    if($regionSignupFormOther) {
        $regionSignupFormOther.ajaxChimp({
            url: 'https://airbitz.us3.list-manage.com/subscribe/post?u=af7e442f9bcaaff857bb5da03&amp;id=b7bd36890d',
            callback: afterEmailSubmission
        });
    }




    function checkActive(region) {
        return typeof activeRegions[region] == 'undefined';
    }

    var regionColors = {};

    for (var key in activeRegions) {
        regionColors[key] = '#2299cf';
    }

    var vmapOptions = {
        map: '',
        backgroundColor: 'transparent',
        stroke: '#80c341',
        color: '#fff',
        hoverColor: '#22bbcf',
        selected: {
            fill: '#CA0020'
        },
//        selectedColor: '#2299cf',
        colors: regionColors,
    }

    // set up map options
    var vmapUS = $.extend(true, {}, vmapOptions);
    vmapUS.map = 'us_aea_en'
    var vmapCA = $.extend(true, {}, vmapOptions);
    vmapCA.map = 'ca_lcc_en';
    var vmapEU = $.extend(true, {}, vmapOptions);
    vmapEU.map = 'europe_mill_en';

    // initialize maps
    $('#vmap-us').vectorMap(vmapUS);
    $('#vmap-ca').vectorMap(vmapCA);
    $('#vmap-eu').vectorMap(vmapEU);


    $('#vmap-us, #vmap-ca, #vmap-eu').bind('regionClick.jvectormap', function(event, label, region){
        if( checkActive(label) ){   // regionClick is not active or upcoming
            console.log('OK REQUEST ' + label);
            var regionName = allRegions[label]['name'];
            showRegionSignup();
            $('#area-request').html(regionName).hide().fadeIn('slow');
            $('#area-request-input').val(label);
            $.ajaxSetup({ crossDomain: true });
        } else {
            var urlLocation = activeRegions[label]['search'];
            var searchUrl = 'search?location=' + urlLocation;
            window.location = searchUrl;
        }
    });

    $('#vmap-us, #vmap-ca, #vmap-eu').bind('labelShow.jvectormap', function(event, label, code){
        if( checkActive(code) ){    // regionHover is not active or upcoming
            var regionName = $(label[0]).html();
            label.html('<span class="hover-region-name">' + regionName + '</span><br /><span class="hover-request-text">Click to Request</span>');
        } else {
            var regionName = $(label[0]).html();
            label.html('<span class="hover-region-name">' + regionName + '</span><br /><span class="hover-click-text">Click to Query</span>')
        }
    });


});