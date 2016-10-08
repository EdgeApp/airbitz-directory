 /*Theme Name:  Keylead - Material Design App Landing Template
     Author: Bighero
     Version: 1.0
  */


 $(document).ready(function($) {

     'use strict';

     $(window).load(function() {
         $('#preloader').fadeOut('slow', function() {
             $(this).remove();
         });
     });

     // WOw js
     new WOW().init();

     // Init Material scripts for buttons ripples, inputs animations etc, more info on the next link https://github.com/FezVrasta/bootstrap-material-design#materialjs
     $.material.init();

     // Sticky Navigation
     $("#sticky-nav").sticky({ topSpacing: 0 });

     // Smooth scroll 
     $(function() {
         $('a[href*="#"]:not([data-toggle="tab"])').on('click', function() {
             if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
                 var target = $(this.hash);
                 target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
                 if (target.length) {
                     $('html, body').animate({
                         scrollTop: target.offset().top
                     }, 1000);
                     return false;
                 }
             }
         });
     });


     // Typing text
     $(".animated-text").typed({
         strings: [
             "material design",
             "fully responsive",
             "onepage template.",
             "mobile first",
             "multi-purpose"
         ],
         typeSpeed: 50,
         loop: true,
     });


     // Screenshots slider

     $("#screenshots .container .slider").owlCarousel({
         nav: false,
         dots: false,
         autoPlay: 5000, //Set AutoPlay to 3 seconds 
         items: 4,
         loop: true,
         responsive: {
             0: {
                 items: 2,
                 nav: false
             },
             600: {
                 items: 3,
                 nav: false
             },
             1000: {
                 items: 5,
                 nav: false,
                 loop: false
             }
         }
     });

     // Reveiws

     $("#clients .owl-carousel").owlCarousel({
         loop: true,
         items: 1,
         dots: true,
     });

     $(".clients-logo .slider").owlCarousel({
         nav: false,
         dots: false,
         autoPlay: 3000, //Set AutoPlay to 3 seconds 
         items: 5,
         loop: true,
         responsive: {
             0: {
                 items: 2,
                 nav: false
             },
             600: {
                 items: 3,
                 nav: false
             },
             1000: {
                 items: 5,
                 nav: false,
                 loop: false
             }
         }

     });

     // FORM VALIDATION

     $(".subscribe-form input").jqBootstrapValidation({
         preventSubmit: true,
         submitSuccess: function($form, event) {
             event.preventDefault(); // prevent default submit behaviour
             $.ajax({
                 success: function() {
                     $('#subscribe-success').html("<div class='alert alert-success'>");
                     $('#subscribe-success > .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
                         .append("</button>");
                     $('#subscribe-success > .alert-success')
                         .append("<strong>Your message has been sent. </strong>");
                     $('#subscribe-success > .alert-success')
                         .append('</div>');
                 }
             })

         }
     });

     $("#contactForm input, #contactForm textarea").jqBootstrapValidation({
         preventSubmit: true,
         submitError: function($form, event, errors) {
             // additional error messages or events
         },
         submitSuccess: function($form, event) {
             event.preventDefault(); // prevent default submit behaviour
             // get values from FORM
             var name = $("input#name").val();
             var email = $("input#email").val();
             var message = $("textarea#message").val();
             var firstName = name; // For Success/Failure Message
             // Check for white space in name for Success/Fail message
             if (firstName.indexOf(' ') >= 0) {
                 firstName = name.split(' ').slice(0, -1).join(' ');
             }
             $.ajax({
                 url: "././mail/sendmail.php",
                 type: "POST",
                 data: {
                     name: name,
                     email: email,
                     message: message
                 },
                 cache: false,
                 success: function() {
                     // Success message
                     $('#success').html("<div class='alert alert-success'>");
                     $('#success > .alert-success').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
                         .append("</button>");
                     $('#success > .alert-success')
                         .append("<strong>Your message has been sent. </strong>");
                     $('#success > .alert-success')
                         .append('</div>');

                     //clear all fields
                     $('#contactForm').trigger("reset");
                 },
                 error: function() {
                     // Fail message
                     $('#success').html("<div class='alert alert-danger'>");
                     $('#success > .alert-danger').html("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;")
                         .append("</button>");
                     $('#success > .alert-danger').append("<strong>Sorry " + firstName + ", it seems that my mail server is not responding. Please try again later!");
                     $('#success > .alert-danger').append('</div>');
                     //clear all fields
                     $('#contactForm').trigger("reset");
                 },
             })
         },
         filter: function() {
             return $(this).is(":visible");
         },
     });


 });
