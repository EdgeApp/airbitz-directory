/*jshint devel:true */

$(function() {


    $('select').select2({ 'width': '200px' });

    AB.setup();
    $.ajax({
        dataType: 'json',
        contentType: 'json',
        type: "GET",
        url: "/mgmt/api/cat/?page_size=2000"
    }).done(function(data) {
        var d = data.results.map(function(m) {
            return { id: m.id, text: m.name };
        });
        var startId = 0;
        $('#categories').select2({
            width: '100%',
            multiple: true,
            data : d,
            createSearchChoice: function(term, data) {
                return { id: startId--, text: term };
            }
        });
    });




    // setup interface
    var $addHoursModule = $('.module-add-hours');
    $addHoursModule.hide();

    var $buttonAddHours = $('.button-add-hours');
    $buttonAddHours.hide();


    $('.button-add-hours').on('click', function(e){
        e.preventDefault();
        $addHoursModule.fadeIn();
    });

    $('.module-footer .button-add').on('click', function(e){
        e.preventDefault();
        $addHoursModule.fadeOut();
    });

    $('.module-footer .button-cancel').on('click', function(e){
        e.preventDefault();
        $addHoursModule.fadeOut();
    });




    $('input:radio[name="optionsBizHours"]').on('change',
        function(){
            console.log($(this).val());

            if($(this).val() == 'open') {
                $buttonAddHours.fadeIn();
            } else {
                $buttonAddHours.fadeOut();
                $addHoursModule.fadeOut();
            }
        }
    );



});



