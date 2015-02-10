/* jshint devel:true */

$('.container .video').magnificPopup({type: 'iframe'});

$('.container').fitVids();

$(document).ready(function() {
  $('pre code').each(function(i, block) {
    hljs.highlightBlock(block);
  });
});