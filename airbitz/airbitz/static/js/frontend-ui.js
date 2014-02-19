/*jshint devel:true */

$(function() {

    // ENABLE CALLBACK FOR SHOW AND HIDE ON BOOTSTRAP TOOLTIPS AND POPOVERS
    var tmpPopoverShow = $.fn.popover.Constructor.prototype.show;
    $.fn.popover.Constructor.prototype.show = function () {
        tmpPopoverShow.call(this);
        if (this.options.callbackShow) {
            this.options.callbackShow();
        }
    };
    var tmpPopoverHide = $.fn.popover.Constructor.prototype.hide;
    $.fn.popover.Constructor.prototype.hide = function () {
        tmpPopoverHide.call(this);
        if (this.options.callbackHide) {
            this.options.callbackHide();
        }
    };
    var tmpTooltipShow = $.fn.tooltip.Constructor.prototype.show;
    $.fn.tooltip.Constructor.prototype.show = function () {
        tmpTooltipShow.call(this);
        if (this.options.callbackShow) {
            this.options.callbackShow();
        }
    };
    var tmpTooltipHide = $.fn.tooltip.Constructor.prototype.hide;
    $.fn.tooltip.Constructor.prototype.hide = function () {
        tmpTooltipHide.call(this);
        if (this.options.callbackHide) {
            this.options.callbackHide();
        }
    };


    // NAVBAR SEARCH HELP/TIPS
    $('#help-search').popover({
        show: true,
        trigger: 'hover',
        placement: 'bottom',
        title: 'Search Tips',
        content:    'Search for <strong class="primary">Business Names</strong> like "<strong class="info">Pangea Bakery</strong>"<br />' +
                    'Search for <strong class="primary">Business Categories</strong> like "<strong class="info">restaurant</strong>"<br /><hr />'+
                    'Search near <strong class="primary">City</strong> or <strong class="primary">State</strong> or <strong class="primary">Zip</strong><br />' +
                    'Ex. <strong class="info">San Diego</strong> or <strong class="info">Ca</strong> or <strong class="info">92101</strong>',
        html: true,
        callbackShow: function() {
            $('.biz-info-two #map').slideToggle();
        },
        callbackHide: function() {
            $('.biz-info-two #map').slideToggle();
        }
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
        height: parseInt( $('.biz-name').css('line-height'), 10) * 2, //this is the line height
        ellipsis: ' ...',
        wrap: 'letter',
        watch: true,
    });



    // hide but make description expandable on biz info page
    $('.biz-info-two .biz-description').readmore({
        maxHeight: parseInt( $('.biz-description').css('line-height'), 10) * 5 //this is the line height
    });





});