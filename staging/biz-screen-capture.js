 /* jshint ignore:start */

var casper = require('casper').create();

var args = casper.cli.args;

var captureDir = '/staging/media/screencaps/';
var baseSite = 'http://127.0.0.1:8000';
var bizPage = baseSite + '/biz/';

var urls = [];

if (args.length < 1) {
	casper
		.echo('Usage: $ casperjs biz-screen-capture.js id1 id2 id3 ..')
		.exit(1);

} else if (args.length >= 1) {
	for (ii=0; ii<args.length; ii++) {
		var bizId = args[ii].toString();
		urls[ii] = bizPage + bizId;
		casper.echo(urls[ii]);
	}
}

casper.start();

casper.each(urls, function(self, urls) {
    this.clear();

    var url = urls
    var bizId = url.split("/")[4];

    this.then(function() {
    	this.viewport(1300, 900);
    });

    this.thenOpen(url, function() {

		if (this.currentHTTPStatus === 404) {
            this.warn(url + ' is missing (HTTP 404)');

        } else if (this.currentHTTPStatus === 500) {
            this.warn(url + ' is broken (HTTP 500)');

        } else {
            this.then(function() {
	            this.echo(url + ' is okay (HTTP ' + this.currentHTTPStatus + ')');
	            this.echo(this.getTitle());
            });

            this.wait(1000);

			this.thenEvaluate(function() {				
				// $('body').css({
				// 	'padding-top': '145px', 
				// });
				// $('#nav-desktop').children().remove(); // hide navbar
				// $('#nav-desktop').append('<img id="new-logo" style="margin: 10px; height: 100px;" src="' + baseSite + '/static/img/logo.png" />');
				// $('#nav-desktop').css({
				// 	'text-align': 'center', 
				// 	'border-top': '1px solid #999',
				// 	'border-left': '1px solid #999',
				// 	'border-right': '1px solid #999',
				// });
				$('#nav-desktop').css({'display':'none !important',});
				$('.addthis-smartlayers').hide(); // hide social sharing buttons
				$('colgroup col').css('border', 'none'); // remove day highlighting

			});
			
			this.wait(1000);

			this.then(function() {
				
				this.echo('SCREENSHOT[' + bizId + ']: ' + url);
			    this.capture(captureDir + 'biz-' + bizId + '.jpg', {
			        format: 'jpg',
			        quality: 100,
			        top: 0,
			        left: 0,
			        width: 1300,
			        height: 825,
			    });

			});
        }
    });
});





casper.run();
/* jshint ignore:end */