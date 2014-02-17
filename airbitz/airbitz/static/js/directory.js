$(function() {

    // RATINGS WIDGET
    // https://github.com/wbotelhos/raty
    $('.star').raty('set',{
        starOn:     '/static/extras/raty-master/lib/images/star-on.png',
        starOff:    '/static/extras/raty-master/lib/images/star-off.png',
        starHalf:   '/static/extras/raty-master/lib/images/star-half.png',
        half:       true
    });


    // SEARCH TOGGLE DISPLAY
    $('#list').click(function(event){
        event.preventDefault();
        $('.results-grid .item').addClass('list-group-item');
    });
    $('#grid').click(function(event){
        event.preventDefault();
        $('.results-grid .item').removeClass('list-group-item');
        $('.results-grid .item').addClass('grid-group-item');
    });




    // ENABLE BIZ LIGHTBOX GALLERY
    $('.swipebox').swipebox();




});