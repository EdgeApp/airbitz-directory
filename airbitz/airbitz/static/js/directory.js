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

    // hide the long text areas for search results this will standarize their height
    $('.results-grid .biz-description').dotdotdot({
        height: parseInt( $('.biz-description').css('line-height'), 10) * 5, //this is the line height
        ellipsis: ' ...',
        wrap: 'word',
        watch: true
    });

    $('.results-map-list .biz-description').dotdotdot({
        height: parseInt( $('.biz-name').css('line-height'), 10) * 2, //this is the line height
        ellipsis: ' ...',
        wrap: 'letter',
        watch: true
    });



    // SINGLE LISTINGS

    /* enable biz lightbox gallery */
    $('.swipebox').swipebox();

    // hide but make description expandable on biz info page
    $('.biz-info-two .biz-description').readmore({
        maxHeight: parseInt( $('.biz-info-two .biz-description').css('line-height'), 10) * 5 //this is the line height
    });


    $('.biz-address-street').dotdotdot({
        height: parseInt( $('.biz-address-street').css('line-height'), 10) * 2, //this is the line height
        ellipsis: ' ...',
        wrap: 'letter',
        watch: true
    });



});