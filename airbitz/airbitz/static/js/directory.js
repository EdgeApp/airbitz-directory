/*jshint devel:true */

var screen_lg = "screen and (min-width: 992px)";

function getDayOfWeek(day){
    // if no day is given use today
    day = typeof day === 'undefined' ? day = new Date().getDay() : day;
    switch (day)
    {
        case 0:
            name = 'Sunday';
            index = 0;
            break;
        case 1:
            name = 'Monday';
            index = 1;
            break;
        case 2:
            name = 'Tuesday';
            index = 2;
            break;
        case 3:
            name = 'Wednesday';
            index = 3;
            break;
        case 4:
            name = 'Thursday';
            index = 4;
            break;
        case 5:
            name = 'Friday';
            index = 5;
            break;
        case 6:
            name = 'Saturday';
            index = 6;
            break;
    }
    day = {
        'name': name,
        'index': index,
        'short': name.substring(0,3)
    }
    return day;
}

var dayName = getDayOfWeek();


$(function() {

    // ALL DIRECTORY PAGES
    $('.single-line').each(function(){
        var lines = 1;
        var lineHeight = $(this).css('line-height');
        $(this).dotdotdot({
            height: parseInt( lineHeight, 10) * lines, //this is the line height
            ellipsis: ' ...',
            wrap: 'letter',
            watch: true
        });
    });

    // SEARCH AND NEARBY GRID
    $('.results-map-list .biz-address-street').dotdotdot({
        height: parseInt( $('.results-map-list .biz-address-street').css('line-height'), 10) * 1, //this is the line height
        ellipsis: ' ...',
        wrap: 'letter',
        watch: true
    });

    $('.results-map-list .biz-description').dotdotdot({
        height: parseInt( $('.results-map-list .biz-description').css('line-height'), 10) * 3, //this is the line height
        ellipsis: ' ...',
        wrap: 'letter',
        watch: true
    });

    $('.results-map-list .biz-description').css({'opacity': 1}); // hidden until dotdotdot runs then we show...so text isn't overflowing



    // hide the long text areas for search results this will standarize their height
    $('.results-grid .biz-description').dotdotdot({
        height: parseInt( $('.results-grid .biz-description').css('line-height'), 10) * 5, //this is the line height
        ellipsis: ' ...',
        wrap: 'word',
        watch: true
    });

    $('.results-grid .biz-description').css({'opacity': 1}); // hidden until dotdotdot runs then we show...so text isn't overflowing



    // SINGLE LISTINGS

    /* enable biz lightbox gallery */
    $('.swipebox').swipebox();

    // hide but make description expandable on biz info page
    $('.biz-info-two .biz-description').readmore({
        maxHeight: parseInt( $('.biz-info-two .biz-description').css('line-height'), 10) * 5 //this is the line height
    });

    $('.biz-info-two .biz-description').css({'opacity': 1}); // hidden until readmore runs then we show...so text isn't overflowing


    $('.biz-info-two .biz-address-street').dotdotdot({
        height: parseInt( $('.biz-address-street').css('line-height'), 10) * 2, //this is the line height
        ellipsis: ' ...',
        wrap: 'letter',
        watch: true
    });


    // only blur bg on larger screens
    enquire.register(screen_lg, function() {
        $('.top-bg').blurjs({
            source: '.top-bg',
            radius: 35,
            overlay: '',
            offset: {
                x: 0,
                y: 0
            },
            cache: false // keep false because browser localstorage quota limits get hit
        });
    });




});



// wait for everything to resize and load then call masonry
jQuery(window).on('load', function(){
    var $ = jQuery;


    $('.results-grid').masonry({
        itemSelector: '.biz-result',
        opacity: 1,
        transform: 'scale(1)'
    });

    $('.biz-gallery').masonry({
        itemSelector: '.biz-gallery-img',
        opacity: 1,
        transform: 'scale(1)'
    });


    // only load bg on larger screens
    enquire.register(screen_lg, function() {
        $('.top-bg').fadeIn(800);
    });

    // get day of week and find the correct column and highlight it
    $('.biz-hours').find('col:eq(' + (dayName['index'] + 1) + ')').css(
        {'border': '2px solid #2291CF'}
    );
});