/*jshint devel:true */

$(function() {

    // ALL DIRECTORY PAGES
    $('.single-line').dotdotdot({
        height: parseInt( $('.single-line').css('line-height'), 10) * 1, //this is the line height
        ellipsis: ' ...',
        wrap: 'letter',
        watch: true
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



    // hide the long text areas for search results this will standarize their height
    $('.results-grid .biz-description').dotdotdot({
        height: parseInt( $('.results-grid .biz-description').css('line-height'), 10) * 5, //this is the line height
        ellipsis: ' ...',
        wrap: 'word',
        watch: true
    });




    // SINGLE LISTINGS

    /* enable biz lightbox gallery */
    $('.swipebox').swipebox();

    // hide but make description expandable on biz info page
    $('.biz-info-two .biz-description').readmore({
        maxHeight: parseInt( $('.biz-info-two .biz-description').css('line-height'), 10) * 5 //this is the line height
    });


    $('.biz-info-two .biz-address-street').dotdotdot({
        height: parseInt( $('.biz-address-street').css('line-height'), 10) * 2, //this is the line height
        ellipsis: ' ...',
        wrap: 'letter',
        watch: true
    });



});