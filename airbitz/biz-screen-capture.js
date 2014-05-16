/* jshint ignore:start */
//
// Usage: $ casperjs biz-screen-capture.js --url=http://targeturl.com --save=/path/to/save/ id1 [id2 id3 ..]
//
// # Caveats: Seems to fail after processing 10-15 ids
// # ...best to loop with python and call 1 id at a time
// # python example:
// import subprocess
// 



var casper = require('casper').create({
	// verbose: true,
	// logLevel: "debug"
});

var args = casper.cli.args;

// var captureDir = '/staging/media/screencaps/';
var captureDir = casper.cli.has('save') ? casper.cli.get('save') : '/staging/media/screencaps/';
var baseSite = casper.cli.has('url') ? casper.cli.get('url') : 'http://127.0.0.1:8000';
var bizPage = baseSite + '/biz/';

var urls = [];

if (args.length === 0) {
	casper
		.warn('Usage: $ casperjs biz-screen-capture.js --url=http://targeturl.com --save=/path/to/save/ id1 [id2 id3 ..]')
		.exit(1);

} else if (args.length >= 1) {
	if (casper.cli.has('url')) {
		if (casper.cli.get('url')) {
			casper.cli.drop('url');
		}
	}
	if (casper.cli.has('save')) {
		if (casper.cli.get('save')) {
			casper.cli.drop('save');
		}
	}

	for (ii=0; ii<args.length; ii++) {
		var bizId = args[ii].toString();
		urls[ii] = bizPage + bizId;
	}
	casper.warn('**** Processing: ' + urls.length + ' URLS ****');
	casper.warn('IDS: ' + urls[0] + ' - ' + urls[urls.length - 1]);
}


function sayCheese() {
	// Can't figue out how to call this from 

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
}


casper.start();
casper.viewport(1300, 900);
casper.each(urls, function(self, url) {
    var bizId = url.split("/")[4];

    self.thenOpen(url, function() {

		if (self.currentHTTPStatus === 404) {
            self.warn(url + ' is missing (HTTP 404)');

        } else if (self.currentHTTPStatus === 500) {
            self.warn(url + ' is broken (HTTP 500)');

        } else {
            self.then(function() {
	            self.echo(url + ' is okay (HTTP ' + self.currentHTTPStatus + ')');
	            self.echo(self.getTitle());
            });
        }
    });

    self.wait(1000);

	self.thenEvaluate(function() {				
		$('#nav-desktop').css({'display':'none !important',});
		$('.addthis-smartlayers').hide(); // hide social sharing buttons
		$('colgroup col').css('border', 'none'); // remove day highlighting	
	});
	
	self.wait(1000);

	self.then(function() {
		
		self.warn('[' + bizId + ']: SCREEN CAPTURED - ' + url);
	    self.capture(captureDir + 'biz-' + bizId + '.jpg', {
	        format: 'jpg',
	        quality: 100,
	        top: 0,
	        left: 0,
	        width: 1300,
	        height: 825,
	    });

	});

});

casper.run();


/* jshint ignore:end */