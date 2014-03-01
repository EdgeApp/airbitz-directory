/*jshint devel:true */

$(function() {

    // custom holder theme for missing images
    Holder.add_theme("ab-blue", { background: "#428bca", foreground: "white", size: 12}).run();

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
        },
        callbackHide: function() {
        }
    });

    $('#term, #near').on('click', function(){
        $('.tooltip').hide();
    });



});