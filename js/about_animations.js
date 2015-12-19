

$(document).ready(function(){
	// TOC AFFIX
		// CODE CITATION IN ABOUT.CSS
	var affixNav = function(){
		$('#sidebar').affix({
			offset: {top: function(){return $('#sidebarHeight').offset().top-20}}
		});	
	}
	// AFFIXING TO HANDLE SCREEN ZOOM/RESIZE
	affixNav();

	// TOC COLOR UPDATE
	$('.anav').on("click",function(){
		$('.anav').each(function(i,d){
			console.log($(d).prop("class"))
		})
	})

	$('#flux').bind('scroll', function() {
        if($(this).scrollTop() + $(this).innerHeight() >= this.scrollHeight) {
            alert('end reached');
        }
    })

	// FadeOut alert container
	$('#alert_container').click(function(){
		$('#alert_container').fadeOut('slow');
	});

	// Reset button functionality
	$('#reset_button').click(function(){
		$('#inputId').val("");
		$('#inputMutation').val("");
		$('#inputPosition').val("");
	})


})