var data_table;
$(document).ready(function(){
    if (sessionStorage.additional_columns == "true") $("#output-header").append("<th>Quality</th>")
	//GENOME AND BUILD SELECTION DISPLAY
	$('#build_selected').text(sessionStorage.build)
	$('#region_selected').text(sessionStorage.region)
	// LOAD TABLE
	$('#output_body').append(sessionStorage.output)
	// If output table is empty, display a warning popup
	if(sessionStorage.output==""){
		$('#outputAlert').fadeIn("slow");
	}

	// SWISSPROT POPUP
	$('table').on("mouseenter mouseleave",'.fa.fa-star',function(e){
		if (e.type=="mouseenter"){
			$(this).tooltip({container: 'body', placement: 'left', title:"Reviewed Swiss-Prot", trigger: 'manual'});	
			$(this).tooltip('show');
		}else{
			$(this).tooltip('hide');
		}
	})
	// Trembl Popup
	$('table').on("mouseenter mouseleave",'.fa.fa-star-o',function(e){
		if (e.type=="mouseenter"){
			$(this).tooltip({container: 'body', placement: 'left', title:"Unreviewed TrEMBL", trigger: 'manual'});	
			$(this).tooltip('show');
		}else{
			$(this).tooltip('hide');
		}
	})


	// FadeOut output alert container
	$('#outputAlert,#inputMappingInfoContainer').click(function(){
		$(this).fadeOut('slow');
	});

	var tooltipShown = false;
	$('table').on("mouseenter mouseleave", '.srcmut', function(e){
		if (e.type == 'mouseenter'){	
			if ($(this).html().search('green')!=-1){
				//Find correct WT
				var correctWT = ($(this).html().substring(27,28))
				var originalWT = $(this).html().substring(60,61)
				$(this,'.srcmutText').tooltip({container: 'body', placement: 'bottom', title: 'Incorrect wild type residue (' + originalWT + ') given. Assumed correct residue ('+correctWT+').', trigger: 'manual'});	
				$(this, '.srcmutText').tooltip('show');
				tooltipShown = true;
			}
		}
		else if (e.type == 'mouseleave' && tooltipShown){
			$(this, '.srcmutText').tooltip('hide');
		}
	})


	// SHOW #INPUTS->#OUTPUTS POPUP
	var inputElements=[];
	var outputCount=0;
	$('table').find("tr").each(function(x){
		if (x>0){ //Don't want table head
			processingElement=""; //Avoid counting duplicate inputs!
			$(this).find("td").each(function(i,d){
				if(i<3){processingElement+=($(d).text().toLowerCase());}
			})
			if (inputElements.indexOf(processingElement)==-1){inputElements.push(processingElement);}
			outputCount++;
		}
	})
	if (outputCount>0){
		var proper = "inputs";
		var properOutput = "outputs";
		if (inputElements.length==1){proper="input";}
		if (outputCount==1){properOutput="output";}
		$('#mapInfo').text(inputElements.length + " " + proper +  " mapped to " + outputCount + " " + properOutput);
		$('#inputMappingInfoContainer').fadeIn("slow");
	}


	data_table = $('#output_table').DataTable({"pageLength":25});



})
