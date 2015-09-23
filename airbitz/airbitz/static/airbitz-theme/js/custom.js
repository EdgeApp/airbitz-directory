

(function($){

	console.log('LOADED: Airbitz Theme');

	$('.team-profile.modal a').each(function(){
		$(this).attr('target','_blank');
	});


	// NEWSLETTER SIGNUPS
	$('#inputEmailSignupSuccess').slideUp();

	function afterEmailSubmission(resp){
		console.log('submitted');
		if (resp.result === 'success') {
			$('.email-signup').val('');
			console.log('success');
		}
		if (resp.result === 'error') {
			console.log('failed');
		}
	}

  $('#email-signup-form input').on('click', function() {
		$.ajaxSetup({ crossDomain: true });
		console.log('crossdomain: true');
  });

	$('#email-signup-form').ajaxChimp({
		url: 'https://airbitz.us3.list-manage.com/subscribe/post?u=af7e442f9bcaaff857bb5da03&amp;id=b7bd36890d',
		callback: afterEmailSubmission,
	});


	/*
	 THUMB GALLERY
	 */
	var $thumbGalleryDetail1 = $('#thumbGalleryDetail'),
			$thumbGalleryThumbs1 = $('#thumbGalleryThumbs'),
			flag = false,
			duration = 300;

	$thumbGalleryDetail1
			.owlCarousel({
				items: 1,
				margin: 10,
				nav: true,
				dots: false,
				loop: true,
				navText: []
			})
			.on('changed.owl.carousel', function(e) {
				if (!flag) {
					flag = true;
					$thumbGalleryThumbs1.trigger('to.owl.carousel', [e.item.index, duration, true]);
					flag = false;
				}
			});

	$thumbGalleryThumbs1
			.owlCarousel({
				margin: 15,
				items: 4,
				nav: false,
				center: false,
				dots: false
			})
			.on('click', '.owl-item', function() {
				$thumbGalleryDetail1.trigger('to.owl.carousel', [$(this).index(), duration, true]);

			})
			.on('changed.owl.carousel', function(e) {
				console.log(e);
			})
			.on('changed.owl.carousel', function(e) {
				if (!flag) {
					flag = true;
					$thumbGalleryDetail1.trigger('to.owl.carousel', [e.item.index, duration, true]);
					flag = false;
				}
			});

}).apply(this, [jQuery]);

