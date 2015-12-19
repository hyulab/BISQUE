// GLOBALS
var vcfDetected=false;
var currentGenomeBuild="new";
var xcds=false;
var testing;


var changeBuild = function(bld, loadType){
	localStorage["build"]=bld;
	currentGenomeBuild=bld; //Variable passed into cgi execution to determine build
	// Change build display text
	if (bld=="new"){
		$('#currentBuild').text("GRCh38");
        $('#chrBuildSingle').text("GRCh38 Chromosome").attr("onclick","loadXMLdoc('hg38')");
        $('#chrBuildBatch').text("GRCh38 Chromosome").attr("onclick","loadXMLdocBatch('hg38')");
	}
	else if (bld=="old"){
		$('#currentBuild').text("GRCh37");
        $('#chrBuildSingle').text("GRCh37 Chromosome").attr("onclick","loadXMLdoc('hg19')");
        $('#chrBuildBatch').text("GRCh37 Chromosome").attr("onclick","loadXMLdocBatch('hg19')");
	}
}

function changePosition(pos_option) {
    if (pos_option == "cdna") {
        xcds = true;
        $("#transcript-positions").text("cDNA");
    } else {
        xcds = false;
        $("#transcript-positions").text("CDS");
    }
    localStorage["xcds"] = xcds;
}

// RESTORING BATCH STATE UPON CLICKING BACK IN WEB BROWSER
if (localStorage["batchOpen"]=="y"){
	$(".single-input").toggle()
	$('#batch_input_container').toggle()
}



$(document).ready(function(){
    console.log("TEST", localStorage["xcds"])
	// HEADER SQUASH HANDLING ON PAGE LOAD
	if(localStorage['batchOpen']=="y"){
		$('#squash').hide();
	}
	//CDS CHECKBOX HANDLING
	$('#check_me').on("click",function(){
		xcds=!($(this).prop('checked'));
		localStorage["xcds"]=xcds;
	})
    //TRANSCRIPT POSITION RECOVERY HANDLING
    if (localStorage["xcds"] == "true") {
        changePosition("cdna")
    } else if (localStorage["xcds"] == "false") {
        changePosition("cds")
    }
    //GENOME BUILD RECOVERY HANDLING
    changeBuild(localStorage["build"])
	// TIPPED FOR ADVANCED INFO
    Tipped.create("#build_info", "<p style='font-size:15px'>Please choose your preferred genome build.</p>", {position:"bottom",maxWidth:300})
    Tipped.create("#cds_info", "<p style='font-size:15px'>Please choose whether transcript positions (both input and output) should be 1-indexed from the coding region (CDS) or from the entire transcript including UTRs (cDNA).</p>", {position:"bottom",maxWidth:300})
    Tipped.create("#quality_info", "<p style='font-size:15px'>Display identifier alignment scores averaged over all steps of conversions for which alignments are performed.</p>", {position:"bottom",maxWidth:300})
    Tipped.create("#swissprot_info", "<p style='font-size:15px'>Only return UniProt identifiers from the Swiss-Prot database and their associated transcripts.</p>", {position:"bottom",maxWidth:300})
    Tipped.create("#canonical_info", "<p style='font-size:15px'>Only return canonical UniProt identifiers and their associated transcripts.</p>", {position:"bottom",maxWidth:300})


	// TURNING WRAP OFF IF PAGE LOAD AND VALUE IN BATCH INPUT IS NOT NULL
	if ($('#batch_input').val()!=""){$('#batch_input').attr("wrap","off")}

	// VCF BATCH RECOGNITION
	$('#batch_input').on("input loadFile reset itemLoad", function(e){
		if ($('#batch_input').val()!=""){$('#batch_input').attr("wrap","off")}
		if (e.type=="loadFile" || e.type=="reset" || e.type=="itemLoad"){
			//Undoing visual results of verification 
			$('#batchError').find('div').html(""); $('#batchError').hide()
			$('#inputLoading2').hide();
			$('textarea').highlightTextarea('destroy');
		}
		var lines=$('#batch_input').val().split('\n')
		vcfMatch=true;
		var counter=0;
		for (var i=0; i<lines.length; i++){
			if (lines[i]==""){continue;} 
			else if (lines[i][0]=="#"){continue;}
			if (!(lines[i].match(/^([xy0-9\.])+\s{1,8}[0-9\.]+\s{1,8}[a-z0-9\.]{1,40}\s{1,8}[a-z*\.]+\s{1,8}[a-z*\.]+(,[a-z*\.]+)*($|\s{1,8})/i))){
				vcfMatch=false;
			}else{counter++;}
		}
		if(counter==0){vcfMatch=false;}
		if (vcfMatch){
			$('#formatContainer').fadeIn('fast');
		}else{
			$('#formatContainer').fadeOut('fast');
		}
		vcfDetected=vcfMatch;
	})
	$('#batch_input').trigger("itemLoad")
	// VCF BATCH RECOGNITION COMPLETE

	// DRAG-N-DROP BATCH FILE
	$('#batch_input').on(
	    'dragover',
	    function(e) {
	        e.preventDefault();
	        e.stopPropagation();
	    }
	)
	$('#batch_input').on(
	    'dragenter',
	    function(e) {
	        e.preventDefault();
	        e.stopPropagation();
	    }
	)
	$('#batch_input').on("drop", function(e){
		e.preventDefault();
        // e.stopPropagation();
        file=e.originalEvent.dataTransfer.files[0]
        var reader = new FileReader();
		reader.onload = function(e) {
			$('#batch_input').val($('#batch_input').val() + reader.result)
			$('#batch_input').trigger("loadFile")
		}

		reader.readAsText(file);
	})
	// BATCH INPUT WRAP HANDLING
	$('#batch_input').on("focus blur", function(e){
		if (e.type=="focus"){
			$(this).attr("placeholder","")
			$(this).attr("wrap","off");
		}
		else if (e.type=="blur"){
			if ($(this).val()==""){
				$(this).attr("wrap","on")
				$(this).attr("placeholder","Upload a file or manually enter your inputs in one or more of the formats listed in the instructions. *Please limit your queries to 1000 lines");
			}
		}
	})

	// BRAND LOGO HIGHLIGHTING
	$('#brandLogo').on("mouseenter mouseleave", function(e){
		if(e.type=="mouseenter"){$('img', this).css("opacity", '1.0');}
		else if(e.type=="mouseleave"){$('img',this).css("opacity",'0.4')}})


	// EXAMPLE FILE LOGIC BATCH INPUT
	$('#example_file').on("click", function(){
		$.get('misc/batchExample.txt', function(data){$('#batch_input').val(data);})
		$('#batch_input').trigger("loadFile")
	})
	$('#reset_file').on("click", function(){
		$('#batch_input').val("");
		$('#fileInput').val("");
		$('#batch_input').trigger("reset")
		$('#batch_input').prop("wrap","true")
		// $('#batch_input').prop("wrap","false")
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

	$("#add_id_button").click(function(){
		$('.single-input').slideToggle('slow')
		$('#batch_input_container').slideToggle('slow')
		// $('#welcome').slideToggle('slow');
		$('#squash').slideToggle('slow');
		localStorage['batchOpen']="y"
		console.log(localStorage['batchOpen'])
	})

	$('#return_button').click(function(){
		$('#batch_input_container').slideToggle('slow')
		$('.single-input').slideToggle('slow')
		$('#squash').slideToggle('slow');
		localStorage['batchOpen']="n"
		console.log(localStorage['batchOpen'])
	})

})
