$.domReady(function()
{

	$('#contents').bind('click', toggle_menu);
	$('#menu').hide();

	function toggle_menu()
	{
		var current_state = $('#menu').hasClass('open');

		if(current_state == true)
		{
			$('#menu').hide();
			$('#contents, #menu').removeClass('open');
		}
		else
		{
			$('#menu').show();
			$('#contents, #menu').addClass('open');
		}
	}

})
