function afterEmailSubmission(i){"success"===i.result&&($(".inputEmail").val(""),$(".inputText").val(""))}jQuery(function($){function i(){$("#who-accepts-bitcoin").hide(),$("#accepting-bitcoin").css("visibility","visible"),$("#accepting-bitcoin").addClass("animated bounceInDown"),s("accepting-bitcoin",1)}function s(i,s){var n=$.cookie(i,Number)||0,e=++n;$.cookie(i,e,{expires:s})}$("#email-signup-form").on("click",function(){$.ajaxSetup({crossDomain:!0})}),$("#email-signup-form").ajaxChimp({url:"https://airbitz.us3.list-manage.com/subscribe/post?u=af7e442f9bcaaff857bb5da03&amp;id=b7bd36890d",callback:afterEmailSubmission}),$("#app-demo-slides").mouseenter(function(){$("#see-app-in-action").css("visibility","visible"),$("#see-app-in-action").addClass("bounceInDown")}),$("#see-app-in-action").jqueryVideoLightning({autoplay:1,backdrop_opacity:.8}),$("#app-demo-slides").carouFredSel({width:238,height:360,auto:{play:!0},scroll:{pauseOnHover:!0,fx:"crossfade",duration:800,onBefore:function(){$("#see-app-in-action").css("visibility","hidden"),$("#see-app-in-action").removeClass("pulse")}}}),setTimeout(function(){var i=$("#app-store-links"),s=$(".iphone-slider");$(".landing-module").backstretch("resize"),$(".et_pb_slide_image").show(),i.css("visibility","visible"),i.addClass("slideInLeft"),s.css("visibility","visible"),s.addClass("animated bounceInDown")},1250),$(".ab-app-cta .app-install").hover(function(){$(this).find(".app-store").css({zoom:"110%",transition:"all .25s","-webkit-transition":"all .25s","-moz-transition":"all .25s","-0-transition":"all .25s"})},function(){$(this).find(".app-store").css({zoom:"100%"})}),$.cookie("accepting-bitcoin",Number)>1?i():($("#who-accepts-bitcoin").css("visibility","visible"),$("#reveal-who-accepts-bitcoin").mouseenter(function(){i()})),$("#jump-who-accepts-bitcoin").on("click",function(){return i(),$("html, body").animate({scrollTop:0},"slow"),$("#accepting-bitcoin").removeClass("animated bounceInDown pulse"),setTimeout(function(){$("#accepting-bitcoin").addClass("animated pulse")},750),!1}),$(window).scroll(function(){var i=$(window).scrollTop();i>50?(console.log("show"),$("#nav-desktop").css({visibility:"visible"})):$("#nav-desktop").css({visibility:"hidden"})})});