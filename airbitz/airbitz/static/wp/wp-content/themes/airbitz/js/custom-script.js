jQuery(document).ready(function($){
	

	// gravity forms customization for removing default input values (add class "clear_field" to target gravity form elements)
	$('#field_1_1 label, #field_3_1 label').hide();

	$(".clear_field input, .clear_field textarea").focus(function () {
		var origval = $(this).val();
		$(this).val("");
		//console.log(origval);
		$(".clear_field input, .clear_field textarea").blur(function () {
			if($(this).val().length === 0 ) {
				$(this).val(origval);
				origval = null;
			}else{
				origval = null;
			}
		});
	});


	$('#gform_wrapper_3 .gform_footer').appendTo('#gform_wrapper_3 .gform_body');



});