/*jshint devel:true */

$(function() {

    $('#term').tooltip({
        show: true,
        placement: 'bottom',
        title:  'Search for <strong class="primary">Business Names</strong> like "<strong class="info">Pangea Bakery</strong>"<br />' +
                'Search for <strong class="primary">Business Categories</strong> like "<strong class="info">restaurant</strong>"<br />',
        html: true
    });

    $('#near').tooltip({
        show: true,
        placement: 'bottom',
        title:  'Search near <strong class="primary">City</strong> or <strong class="primary">State</strong> or <strong class="primary">Zip</strong><br />' +
                'Ex. <strong class="info">San Diego</strong> or <strong class="info">Ca</strong> or <strong class="info">92101</strong>',
        html: true
    });

    $('#term, #near').on('click', function(){
        $('.tooltip').hide();
    });


    $('.single-line').dotdotdot({
        height: parseInt( $('.biz-name').css('line-height'), 10) * 1, //this is the line height
        ellipsis: ' ...',
        wrap: 'letter',
        watch: true,
    });

    // hide the long text areas for search results this will standarize their height
    $('.results-grid .biz-description').dotdotdot({
        height: parseInt( $('.biz-description').css('line-height'), 10) * 5, //this is the line height
        ellipsis: ' ...',
        wrap: 'word',
        watch: true,
        after: '.view-details'
    });

    $('.results-map-list .biz-description').dotdotdot({
        height: parseInt( $('.biz-name').css('line-height'), 10) * 3, //this is the line height
        ellipsis: ' ...',
        wrap: 'letter',
        watch: true,
    });



    // hide but make description expandable on biz info page
    $('.biz-info-two .biz-description').readmore({
        maxHeight: parseInt( $('.biz-description').css('line-height'), 10) * 5 //this is the line height
    });





});