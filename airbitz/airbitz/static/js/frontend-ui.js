/*jshint devel:true */

var screen_lg = "screen and (min-width: 992px)";
var blurRadius = 10;

function scrollTop(distance) {
    $("html, body").animate({ scrollTop: distance }, "slow");
}

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
                    'Search near <strong class="primary">City</strong>, <strong class="primary">State</strong> or <strong class="primary">Country</strong><br />' +
                    'Ex. <strong class="info">San Diego</strong> or <strong class="info">Ca</strong>',
        html: true,
        callbackShow: function() {
        },
        callbackHide: function() {
        }
    });


    $('.navbar-admin .close').on('click', function() {
        $(this).parents().eq(3).fadeOut();
    });


    $('body').on('click', '#nav-mobile .form-group.term', function() {
        $('#nav-mobile #mobile-nav-close').slideDown();
        $('#nav-mobile .form-group.location').slideDown();
        $('#nav-mobile #mobile-submit').slideDown();

        if( !$('.mobile-app-download').is(':visible') ) {
          $('body').css('margin-top', '30px');
        }
    });


    $('body').on('click', '#nav-mobile #mobile-nav-close', function() {
        $('#nav-mobile #mobile-nav-close').hide();
        $('#nav-mobile .form-group.location').slideUp();
        $('#nav-mobile #mobile-submit').slideUp();
        $('body').css('margin-top', '0');
    });


    if(!bowser.ipad){
        $('.top-bg').css({
            '-webkit-filter': 'blur(25px)',
            '-moz-filter': 'blur(25px)',
            '-o-filter': 'blur(25px)',
            '-ms-filter': 'blur(25px)',
            'filter': 'blur(25px)'
        });
    }


    // only blur bg on larger screens

    if(!Modernizr.webgl) {
        enquire.register(screen_lg, function() {
            var $topBg = $('.top-bg');

            if($topBg.length != 0) {
                $topBg.css({
                    '-webkit-filter': 'blur(' + blurRadius + 'px)',
                });
                $topBg.blurjs({
                    source: '.top-bg',
                    radius: blurRadius,
                    overlay: '',
                    offset: {
                        x: 0,
                        y: 0
                    },
                    cache: false // keep false because browser localstorage quota limits get hit
                });
            }
        });
    }

});







// wait for everything to resize and load then do stuff
jQuery(window).on('load', function(){

  // only load bg on larger screens
  enquire.register(screen_lg, function() {
      $('.top-bg').fadeIn(800);
  });

  $('.top-bg-noblur').fadeIn(800);

});