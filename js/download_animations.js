
$(document).ready(function(){

	//Popup tips over button hover
	//Lite button popover
	Tipped.create('#lite', '<h3>BISQUE Lite</h3><p style="font-size:14px">BISQUE Lite \
		is the recommended installation. <br>At only 30kb, \
		it is <em>extremely</em> lightweight.</p>\
		<h4>Requirements:</h4>\
		<ul><li style="font-size:14px">Ubuntu 12.0.4 or later</li><li style="font-size:14px">A stable internet connection</li>\
		</ul>', {position: 'bottom'});
	//Full button popover
	Tipped.create('#full', '<h3>BISQUE Full</h3><p style="font-size:14px">BISQUE Full is for\
		advanced users only. It allows<br>for a much greater amount of customization<br>and full control\
		over data.\
		<h4>Requirements:</h4>\
		<ul>\
		<li style="font-size:14px">Ubuntu 12.0.4 or later</li>\
		<li style="font-size:14px">At least 4GB of available space</li></ul>', {position: 'bottom'});
	Tipped.create('#github', '<h3>GitHub</h3><p style="font-size:14px">Click to view the BISQUE project on GitHub.<br>\
		There, you can view my source code as well<br>as fork the project to make your own<br> modifications!</p>', {position: 'bottom'});

	$('.btn').mouseenter(function(){
		$(this).toggleClass('bordered-button');
	})
	$('.btn').mouseleave(function(){
		$(this).toggleClass('bordered-button');
	})

	
	
})