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

});