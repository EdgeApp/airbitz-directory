$(function() {


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