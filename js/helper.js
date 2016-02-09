// GLOBALS
var idtype;
var chrs = ['CHR1', 'CHR10', 'CHR11', 'CHR12', 'CHR13', 'CHR14', 'CHR15', 'CHR16', 'CHR17', 'CHR18', 'CHR19', 'CHR2', 'CHR20', 'CHR21', 'CHR22', 'CHR3', 'CHR4', 'CHR5', 'CHR6', 'CHR7', 'CHR8', 'CHR9', 'CHRMT', 'CHRX', 'CHRY', 'CHR_HG142_HG150_NOVEL_TEST', 'CHR_HG151_NOVEL_TEST', 'CHR_HSCHR10_1_CTG1', 'CHR_HSCHR10_1_CTG2', 'CHR_HSCHR10_1_CTG4', 'CHR_HSCHR11_1_CTG5', 'CHR_HSCHR11_1_CTG6', 'CHR_HSCHR11_1_CTG7', 'CHR_HSCHR11_1_CTG8', 'CHR_HSCHR11_2_CTG1', 'CHR_HSCHR11_2_CTG1_1', 'CHR_HSCHR11_3_CTG1', 'CHR_HSCHR12_1_CTG1', 'CHR_HSCHR12_1_CTG2_1', 'CHR_HSCHR12_2_CTG2', 'CHR_HSCHR12_2_CTG2_1', 'CHR_HSCHR12_3_CTG2', 'CHR_HSCHR12_3_CTG2_1', 'CHR_HSCHR12_4_CTG2', 'CHR_HSCHR12_4_CTG2_1', 'CHR_HSCHR12_5_CTG2', 'CHR_HSCHR12_5_CTG2_1', 'CHR_HSCHR12_6_CTG2_1', 'CHR_HSCHR13_1_CTG1', 'CHR_HSCHR13_1_CTG3', 'CHR_HSCHR14_1_CTG1', 'CHR_HSCHR14_2_CTG1', 'CHR_HSCHR14_3_CTG1', 'CHR_HSCHR14_7_CTG1', 'CHR_HSCHR15_1_CTG1', 'CHR_HSCHR15_1_CTG3', 'CHR_HSCHR15_1_CTG8', 'CHR_HSCHR15_2_CTG3', 'CHR_HSCHR15_2_CTG8', 'CHR_HSCHR15_3_CTG3', 'CHR_HSCHR15_3_CTG8', 'CHR_HSCHR15_4_CTG8', 'CHR_HSCHR15_5_CTG8', 'CHR_HSCHR16_1_CTG1', 'CHR_HSCHR16_1_CTG3_1', 'CHR_HSCHR16_2_CTG3_1', 'CHR_HSCHR16_3_CTG1', 'CHR_HSCHR16_4_CTG1', 'CHR_HSCHR16_CTG2', 'CHR_HSCHR17_10_CTG4', 'CHR_HSCHR17_1_CTG1', 'CHR_HSCHR17_1_CTG2', 'CHR_HSCHR17_1_CTG4', 'CHR_HSCHR17_1_CTG5', 'CHR_HSCHR17_1_CTG9', 'CHR_HSCHR17_2_CTG1', 'CHR_HSCHR17_2_CTG2', 'CHR_HSCHR17_2_CTG5', 'CHR_HSCHR17_3_CTG2', 'CHR_HSCHR17_4_CTG4', 'CHR_HSCHR17_5_CTG4', 'CHR_HSCHR17_6_CTG4', 'CHR_HSCHR17_7_CTG4', 'CHR_HSCHR17_8_CTG4', 'CHR_HSCHR18_1_CTG1_1', 'CHR_HSCHR18_1_CTG2_1', 'CHR_HSCHR18_2_CTG2', 'CHR_HSCHR18_2_CTG2_1', 'CHR_HSCHR18_ALT21_CTG2_1', 'CHR_HSCHR18_ALT2_CTG2_1', 'CHR_HSCHR19KIR_ABC08_A1_HAP_CTG3_1', 'CHR_HSCHR19KIR_ABC08_AB_HAP_C_P_CTG3_1', 'CHR_HSCHR19KIR_ABC08_AB_HAP_T_P_CTG3_1', 'CHR_HSCHR19KIR_FH05_A_HAP_CTG3_1', 'CHR_HSCHR19KIR_FH05_B_HAP_CTG3_1', 'CHR_HSCHR19KIR_FH06_A_HAP_CTG3_1', 'CHR_HSCHR19KIR_FH06_BA1_HAP_CTG3_1', 'CHR_HSCHR19KIR_FH08_A_HAP_CTG3_1', 'CHR_HSCHR19KIR_FH08_BAX_HAP_CTG3_1', 'CHR_HSCHR19KIR_FH13_A_HAP_CTG3_1', 'CHR_HSCHR19KIR_FH13_BA2_HAP_CTG3_1', 'CHR_HSCHR19KIR_FH15_A_HAP_CTG3_1', 'CHR_HSCHR19KIR_FH15_B_HAP_CTG3_1', 'CHR_HSCHR19KIR_G085_A_HAP_CTG3_1', 'CHR_HSCHR19KIR_G085_BA1_HAP_CTG3_1', 'CHR_HSCHR19KIR_G248_A_HAP_CTG3_1', 'CHR_HSCHR19KIR_G248_BA2_HAP_CTG3_1', 'CHR_HSCHR19KIR_GRC212_AB_HAP_CTG3_1', 'CHR_HSCHR19KIR_GRC212_BA1_HAP_CTG3_1', 'CHR_HSCHR19KIR_LUCE_A_HAP_CTG3_1', 'CHR_HSCHR19KIR_LUCE_BDEL_HAP_CTG3_1', 'CHR_HSCHR19KIR_RP5_B_HAP_CTG3_1', 'CHR_HSCHR19KIR_RSH_A_HAP_CTG3_1', 'CHR_HSCHR19KIR_RSH_BA2_HAP_CTG3_1', 'CHR_HSCHR19KIR_T7526_A_HAP_CTG3_1', 'CHR_HSCHR19KIR_T7526_BDEL_HAP_CTG3_1', 'CHR_HSCHR19LRC_COX1_CTG3_1', 'CHR_HSCHR19LRC_COX2_CTG3_1', 'CHR_HSCHR19LRC_LRC_I_CTG3_1', 'CHR_HSCHR19LRC_LRC_J_CTG3_1', 'CHR_HSCHR19LRC_LRC_S_CTG3_1', 'CHR_HSCHR19LRC_LRC_T_CTG3_1', 'CHR_HSCHR19LRC_PGF1_CTG3_1', 'CHR_HSCHR19LRC_PGF2_CTG3_1', 'CHR_HSCHR19_1_CTG2', 'CHR_HSCHR19_1_CTG3_1', 'CHR_HSCHR19_2_CTG2', 'CHR_HSCHR19_3_CTG2', 'CHR_HSCHR19_3_CTG3_1', 'CHR_HSCHR19_4_CTG2', 'CHR_HSCHR19_4_CTG3_1', 'CHR_HSCHR19_5_CTG2', 'CHR_HSCHR1_1_CTG3', 'CHR_HSCHR1_1_CTG31', 'CHR_HSCHR1_1_CTG32_1', 'CHR_HSCHR1_2_CTG3', 'CHR_HSCHR1_2_CTG31', 'CHR_HSCHR1_2_CTG32_1', 'CHR_HSCHR1_3_CTG31', 'CHR_HSCHR1_3_CTG32_1', 'CHR_HSCHR1_4_CTG31', 'CHR_HSCHR1_ALT2_1_CTG32_1', 'CHR_HSCHR20_1_CTG1', 'CHR_HSCHR20_1_CTG2', 'CHR_HSCHR20_1_CTG3', 'CHR_HSCHR21_2_CTG1_1', 'CHR_HSCHR21_3_CTG1_1', 'CHR_HSCHR21_4_CTG1_1', 'CHR_HSCHR21_5_CTG2', 'CHR_HSCHR22_1_CTG1', 'CHR_HSCHR22_1_CTG2', 'CHR_HSCHR22_1_CTG3', 'CHR_HSCHR22_1_CTG4', 'CHR_HSCHR22_1_CTG5', 'CHR_HSCHR22_1_CTG6', 'CHR_HSCHR22_1_CTG7', 'CHR_HSCHR22_2_CTG1', 'CHR_HSCHR22_3_CTG1', 'CHR_HSCHR2_1_CTG1', 'CHR_HSCHR2_1_CTG5', 'CHR_HSCHR2_1_CTG7_2', 'CHR_HSCHR2_2_CTG7', 'CHR_HSCHR2_2_CTG7_2', 'CHR_HSCHR2_3_CTG15', 'CHR_HSCHR2_3_CTG7_2', 'CHR_HSCHR2_4_CTG1', 'CHR_HSCHR3_1_CTG1', 'CHR_HSCHR3_1_CTG2_1', 'CHR_HSCHR3_1_CTG3', 'CHR_HSCHR3_2_CTG2_1', 'CHR_HSCHR3_2_CTG3', 'CHR_HSCHR3_3_CTG3', 'CHR_HSCHR3_4_CTG2_1', 'CHR_HSCHR3_4_CTG3', 'CHR_HSCHR3_5_CTG3', 'CHR_HSCHR3_6_CTG3', 'CHR_HSCHR3_7_CTG3', 'CHR_HSCHR3_8_CTG3', 'CHR_HSCHR3_9_CTG3', 'CHR_HSCHR4_1_CTG12', 'CHR_HSCHR4_1_CTG6', 'CHR_HSCHR4_1_CTG9', 'CHR_HSCHR4_3_CTG12', 'CHR_HSCHR4_5_CTG12', 'CHR_HSCHR4_6_CTG12', 'CHR_HSCHR4_7_CTG12', 'CHR_HSCHR5_1_CTG1', 'CHR_HSCHR5_1_CTG1_1', 'CHR_HSCHR5_1_CTG5', 'CHR_HSCHR5_2_CTG1', 'CHR_HSCHR5_2_CTG1_1', 'CHR_HSCHR5_2_CTG5', 'CHR_HSCHR5_3_CTG1', 'CHR_HSCHR5_3_CTG5', 'CHR_HSCHR5_4_CTG1', 'CHR_HSCHR5_4_CTG1_1', 'CHR_HSCHR5_5_CTG1', 'CHR_HSCHR5_6_CTG1', 'CHR_HSCHR6_1_CTG2', 'CHR_HSCHR6_1_CTG4', 'CHR_HSCHR6_1_CTG5', 'CHR_HSCHR6_1_CTG7', 'CHR_HSCHR6_1_CTG8', 'CHR_HSCHR6_8_CTG1', 'CHR_HSCHR6_MHC_APD_CTG1', 'CHR_HSCHR6_MHC_COX_CTG1', 'CHR_HSCHR6_MHC_DBB_CTG1', 'CHR_HSCHR6_MHC_MANN_CTG1', 'CHR_HSCHR6_MHC_MCF_CTG1', 'CHR_HSCHR6_MHC_QBL_CTG1', 'CHR_HSCHR6_MHC_SSTO_CTG1', 'CHR_HSCHR7_1_CTG4_4', 'CHR_HSCHR7_1_CTG6', 'CHR_HSCHR7_2_CTG4_4', 'CHR_HSCHR7_2_CTG6', 'CHR_HSCHR7_3_CTG6', 'CHR_HSCHR8_1_CTG1', 'CHR_HSCHR8_1_CTG6', 'CHR_HSCHR8_1_CTG7', 'CHR_HSCHR8_2_CTG7', 'CHR_HSCHR8_3_CTG1', 'CHR_HSCHR8_3_CTG7', 'CHR_HSCHR8_4_CTG7', 'CHR_HSCHR8_5_CTG1', 'CHR_HSCHR8_5_CTG7', 'CHR_HSCHR8_7_CTG1', 'CHR_HSCHR8_8_CTG1', 'CHR_HSCHR8_9_CTG1', 'CHR_HSCHR9_1_CTG1', 'CHR_HSCHR9_1_CTG2', 'CHR_HSCHR9_1_CTG3', 'CHR_HSCHR9_1_CTG4', 'CHR_HSCHR9_1_CTG5', 'CHR_HSCHRX_1_CTG3', 'CHR_HSCHRX_2_CTG12', 'CHR_HSCHRX_2_CTG3', 'GL000008.2', 'GL000009.2', 'GL000194.1', 'GL000195.1', 'GL000205.2', 'GL000213.1', 'GL000216.2', 'GL000218.1', 'GL000219.1', 'GL000220.1', 'GL000224.1', 'GL000225.1', 'KI270442.1', 'KI270706.1', 'KI270707.1', 'KI270708.1', 'KI270711.1', 'KI270713.1', 'KI270714.1', 'KI270721.1', 'KI270722.1', 'KI270723.1', 'KI270724.1', 'KI270726.1', 'KI270727.1', 'KI270728.1', 'KI270731.1', 'KI270733.1', 'KI270734.1', 'KI270741.1', 'KI270743.1', 'KI270744.1', 'KI270750.1', 'KI270752.1']
var single_process;
var batch_process;
var fill_process;

var resize_dropdown = function(){
	if ($(window).height()<=700){
		$('.dropdown-menu').addClass("dover")
	}else if($(window).height()>700){
		$('.dropdown-menu').removeClass("dover")
	}
}

$(document).ready(function(){
	// BRAND LOGO BATCH RESET
	$('#brandLogo').on("click",function(){localStorage["batchOpen"]="n"})

	// WINDOW RESIZING HANDLING SO CONVERT TO DROPDOWN IS NOT CUTOFF AT LOW WINDOW HEIGHTS
	resize_dropdown();
	$(window).resize(function(){
		resize_dropdown();
	})

	// CANCEL QUERY HANDLING
	$('#cancel_query').on("click",function(){
		$('#dimmer').hide();
	})
})


/////////////////////////////////////////////////////
// INPUT VERIFICATION FOR SINGLE AND BATCH QUERIES//
/////////////////////////////////////////////////
function disallow_chromosome(input, position){
	input=input.toUpperCase().replace("CHR","");
	if (chrs.indexOf(("CHR"+input).toUpperCase())!=-1 && !position){
		return "When converting from a chromosome, you must include position."
	}

	return "OK";
}


function verifyInput(){
	var id = document.getElementById("inputId").value;
	var mutation = document.getElementById("inputMutation").value;
	var position = document.getElementById("inputPosition").value;
	//DISSALOW CHROMOSOME
	var dchrom=disallow_chromosome(id,position);
	if (dchrom!="OK"){return dchrom;}
	if(id.length==0){
		return 'You must include an input identifier to convert.';
	}else if (mutation.length>0 && position.length==0){
		return 'You must include a position for your input mutation.';
	// ID MATCHING
	}else if (($('#inputId').popover().attr("alive"))=="false"){
		return "Your input is not recognized as any Ensembl, Uniprot, RefSeq, GRCh38 or Gene Name identifiers."
	// MUTATION MATCHING
	}else if (mutation.match(/^(([a-z*][a-z*](\/[a-z*])*)|([a-z*]->[a-z*])|([a-z*]>[a-z*])|())$/i)==null){
		return "The mutation given as an input is invalid."
	// POSITION MATCHING
	}else if (!position.match(/^(([1-9])|([1-9][0-9]+)|())$/i)){
		return "The position given as an input is invalid. Please keep in mind that all positions are 1-indexed."
	}else if (idtype.search(/protein|pdb/i)==-1 && idtype.search(/reference/i)==-1 && mutation && 
		("ATGC".indexOf(mutation[0].toUpperCase())==-1 || "ATGC".indexOf(mutation.slice(-1).toUpperCase())==-1)){
		return "You cannot assign amino acid bases to a non-protein identifier!"
	 
	}else{return 'OK';}

}

var jumpToError = function(lineNum){
	var lineHeight=parseInt($('#batch_input').css('line-height'));
	$('#batch_input').scrollTop(lineNum*lineHeight);
}


var restrictSize = function(batch_input){
	var lines=batch_input.split('\n')
	if (lines.length>1000){
		$('#batchError').find('div').html("");
		$('#batchError').show();
		$('#batchError').find('div').append("<p>Batch queries are limited to 1000 inputs.</p>")
		return "NO"
	}
	return "YES"
}

var verifyBatch = function(batchInpt,out_type){
	var lines=batchInpt.split("\n");
	var errorList=[]
	var highlight=[];
	for (var i=0; i<lines.length;i++){
		// DISALLOW CHROMOSOME
		if (lines[i].match(/^\s*$/i)){continue;}
		var data = lines[i].split(/[\s,:,\t]+/);
		var dchrom = "OK";
		if (data.length==1){dchrom=disallow_chromosome(data[0],null);}
		//DISALLOW TO/FROM DBSNP W/O POSITION
		var snp_conv="OK";
		if (out_type=="dbsnp" && data.length==1 && data[0].slice(0,2).toLowerCase()!="rs"){snp_conv="NO";} 
		// GENERAL ERROR HANDLING
		if (lines[i]
			.match(/^[^:\s\t,]+([:\s\t,]([0-9]+|[a-z\*][0-9]+[a-z\*]|[0-9]+[:\s\t,][a-z\*][>]{0,1}[a-z\*]|[a-z\*][\.][a-z\*]+[0-9]+[a-z]+|[a-z\*][\.][0-9]+[a-z\*][>]{0,1}[a-z\*])){0,1}$/i)==null || dchrom!='OK' || snp_conv!="OK"){
			if (lines[i]==""){continue;}
			errorList.push(i); console.log(lines[i]);
			highlight.push(lines[i]);
		}
	}
	 $('textarea').highlightTextarea('destroy');
	$('textarea').highlightTextarea({words:highlight,color:'#FFA9A9'});
	if (errorList.length>0){
		$('#batchError').find('div').html("");
		$('#batchError').show();
		$('#batchError').find('div').append("<p>Some of your inputs are invalid.</p>")
		$('#batchError').find('div').append("<p><a style='cursor:pointer' id='continueAnyways' onclick='loadXMLdocBatch(currentOutput,true)'>Click to ignore errors and continue.</a></p>")
		jumpToError(errorList[0]);

	}

	return errorList
	
}



var fill_input = function(output_data, cur_build, batch){	
	if (typeof(batch)=="undefined"){batch="n"}
	url="/cgi-bin/input_fill.cgi";
	$.ajaxSetup({async: false}); //ASYNC FALSE
	result=null;
	fill_process = $.post(url, {
        output: JSON.stringify(output_data), 
        build: String(cur_build), 
        batch: String(batch),
        cdna: xcds
    }, function(data){
		result=data;
	})
	$.ajaxSetup({async: true}); //RESTORE ASYNC
	return result;
}


var dim = function(){
	// DIMMING CREDIT GOES TO:http://stackoverflow.com/questions/9455556/how-can-i-dim-the-rest-of-the-web-page-when-displaying-a-notification-div
		$('<div id="dimmer">').css({
	      "width" : "100%"
	    , "height" : "100%"
	    , "background" : "#000"
	    , "position" : "fixed"
	    , "top" : "0"
	    , "left" : "0"
	    , "zIndex" : "10000"
	    , "MsFilter" : "progid:DXImageTransform.Microsoft.Alpha(Opacity=60)"
	    , "filter" : "alpha(opacity=60)"
	    , "MozOpacity" : 0.6
	    , "KhtmlOpacity" : 0.6
	    , "opacity" : 0.6

	}).appendTo(document.body);


}
/////////////////////////
// QUERY EXECUTION LOGIC/
////////////////////////

//function loadXMLdoc(output) {
function loadXMLdoc(output) {
	var url = "/cgi-bin/run.cgi"
	var id = $.trim(document.getElementById("inputId").value);
	var mutation = document.getElementById("inputMutation").value;
	var position = document.getElementById("inputPosition").value;
	var warningMessage=verifyInput();
    if (warningMessage == "OK") {
        xcds_output="n";
        if (xcds){xcds_output="y";}
        single_process = $.post(url, {
            id: id,
            mutation: mutation,
            position: position,
            output: output,
            build: currentGenomeBuild, 
            xcds: xcds_output,
            quality: $("#quality").prop("checked"),
            canonical: $("#canonical").prop("checked"),
            swissprot: $("#swissprot").prop("checked"),
            web: "n"
        }, function(d) {
            buildTable(d, output);
        }, "json");
        dim();
        $('#inputLoading').css("display","inline-block")
    } else {
		$(document).ready(function(){
			$('#alert_container').find('#wMessage').text(warningMessage);
			$('#alert_container').fadeIn('slow');
		})
    }
}

var currentOutput;
function loadXMLdocBatch(output, bypass) {
	currentOutput=output;
	var verify=[];
	if (typeof(bypass)=='undefined'){bypass=false} //Error bypass option
	var url = "/cgi-bin/batch.cgi"
	var input = document.getElementById("batch_input").value;
	if (restrictSize(input)=="NO"){return;}
	if (vcfDetected){verify = [];}
	else{verify=verifyBatch(input,output);}
	if(input==""){return;}
	// VCF HANDLING
	if (verify.length==0||bypass){
		xcds_output="n"
		if (xcds){xcds_output="y";}
		$.post(url, {
            input: input, output: output, vcf: vcfDetected, build: currentGenomeBuild, xcds: xcds_output,
            swissprot: $("#swissprot").prop("checked"),
            canonical: $("#canonical").prop("checked"),
            quality: $("#quality").prop("checked")
        }, function(data){
            console.log(data)
			buildTable(data, output);
		}, "json")
        .fail(function(x, textstatus, errorthrown) {
            console.log(textstatus)
        })
		dim();
		$('#inputLoading').css("display","inline-block");
	}
}

function buildTable(d, type) {
        var additional_columns = false
        //Backwards conversion if output type is dbsnp
        if(type=="dbsnp"){
            d=fill_input(d, currentGenomeBuild, "n");
        }
        var table_output = "";
        for (var i = 0; i < d.length; i++) {
            var object = d[i];
            if (!object.value) continue;
            var source = "", input_source = "", displayed_key = object.source_id;
            if (type=="dbsnp" && (!object.mutation || !object.position)){continue;} 
            //Exception for dbSNP from PDB
            if (object.snp_source){
                object.source_position=object.snp_source.split('/')[0]; object.source_mutation=object.snp_source.split('/')[1]
            }
            // Wild Type Error handling
            if (object.wt_error){object.source_mutation = "<span style='color:green'>" + "(" + object.wt_error +")" + "</span>" + "<span style='color:red'>" + object.source_mutation[0]+ "</span>" + object.source_mutation.slice(1);}
            // Output Source
            if (object.source == "s"){source="<span class='fa fa-star' style='color:#c0a92f'></span> ";}
            else if (object.source == "t"){source="<span class='fa fa-star-o' style='color:#008B8B'></span> "}
            // Input Source
            if (object.input_source == "s") {input_source="<span class='fa fa-star' style='color:#c0a92f'></span> ";}
            else if (object.input_source == "t") {input_source="<span class='fa fa-star-o' style='color:#008B8B'></span> "}
            // APPEND PDB CHAIN IF NECESSARY
            if (object.chain_source && object.mutation.length == 4) displayed_key += object.chain_source; 
            // REPLACE SOURCE MUTATION WITH SOURCE WILD TYPE IF NECESSARY
            if(!object.source_mutation && object.wt_source) object.source_mutation = object.wt_source;
            // REPLACE OUTPUT MUTATION WITH OUTPUT WILD TYPE IF NECESSARY
            if(!object.mutation && object.wt_out) object.mutation = object.wt_out;
            //Generate source link, depending on if gene name or not
            var sourceLink = object.reference_id ? "<a href='http://www.uniprot.org/uniprot/"+object.reference_id+"'target='_blank'>" + object.source_id + "</a>" : getLink(displayed_key, object.source_position);
            //Generate quality row
            quality_html = "";
            if ($("#quality").prop("checked")) {
                additional_columns = true
                quality_html = "<td>" + object.quality + "</td>";
            }
            // Convert nulls to - for aesthetics
            for (var key in object) {
                if (!object[key]) object[key] = "-";
            }
            //Build HTML Table Row
            table_output+="<tr><td id='srcid'>"+ input_source + sourceLink + "</td><td>" + object.source_position +"</td><td class='srcmut'>" + object.source_mutation + "</td><td>"+source + getLink(object.value, object.position)+"</td><td>" + object.position + "</td><td>" + object.mutation + "</td>" + quality_html + "</tr>"
        }
        sessionStorage.setItem('output', table_output) //Storing output in browser wide variable for output.html
        region_selected="cDNA";
        if(!xcds){region_selected="CDS"}
        build_selected="GRCh38"
        if(currentGenomeBuild=="old"){build_selected="GRCh37"}
        sessionStorage.setItem('build',build_selected);
        sessionStorage.setItem('region',region_selected);
        sessionStorage.setItem("additional_columns", additional_columns);
        window.open('output.html', '_self') //Opening output wi	
}





///////////////////
//LINK GENERATOR//
/////////////////
function getLink(identifier, position){
	identifier = identifier.toUpperCase();
	source=null;
	if (identifier.search(/^enst[0-9]{11,11}$/i) == 0){
		source="enst";
	}
	else if (identifier.search(/^[n,x]M_[0-9]{5,9}.*[0-9]*$/i)==0){
		source='reft';
	}
	else if (identifier.search(/^[n,x]P_[0-9]{5,9}.*[0-9]*$/i)==0){
		source='refp';
	}
	else if (identifier.search(/^[n,x]P_[0-9]{5,9}.*[0-9]*$/i)==0){
		source='refp';
	}
	else if (identifier.search(/^rs[0-9]{3,40}$/i)==0){
		source='dbsnp';
	}
	else if (identifier.search(/^ensp[0-9]{11,11}$/i) == 0){
		source="ensp";
	}
	else if (identifier.search(/^ensg[0-9]{11,11}$/i) == 0){
		source="ensg";
	}
	else if (identifier.search(/^chr.+$/i) == 0){
		source="hg38";
	}
	else if (identifier.search(/^[a-z]\d\w\w\w[0-9][-][0-9]+$/i) == 0){
		source="uniprot";
	}
	else if (identifier.search(/^[0-9][a-z0-9]{3,5}$/i)==0){
		source="pdb";
	}
	else if (identifier.search(/^[a-z]\d\w\w\w[0-9]$/i) == 0){
		source="uniprot";
	}

	else if (identifier.search(/^\d$|^([1]\d$)|^([2][0-2]$)|^x$|^y$/i)==0){
		identifier = "chr" + identifier; source="hg38"
	}

	else if (identifier.search(/^[a-z]{1,1}\w*$/i) == 0){
		source="geneName";
	}


	if (source=="uniprot"){
	    return "<a href='http://www.uniprot.org/uniprot/%s' target='_blank'>".replace('%s', identifier) + identifier + "</a>"; 
	}
	else if (source=="dbsnp"){
		return "<a target='_blank' href='http://www.ncbi.nlm.nih.gov/projects/SNP/snp_ref.cgi?rs=%s'>".replace('%s', identifier) + identifier.toLowerCase() + "</a>"
	}
	else if (source=='geneName'){
		return "<a href='http://www.uniprot.org/uniprot/?query=%s&sort=score' target='_blank'>".replace('%s',identifier)+identifier+"</a>";
	}
	else if (source=="enst"){
		return "<a target='_blank' href='http://www.ensembl.org/Homo_sapiens/Transcript/Summary?t=%s'>".replace('%s', identifier) + identifier + "</a>"
	}
	else if (source=="ensg"){
		return "<a target='_blank' href='http://www.ensembl.org/Homo_sapiens/Gene/Summary?g=%s'>".replace('%s', identifier) + identifier + "</a>"
	}
	else if (source=="pdb"){
		return "<a target='_blank' href='http://www.rcsb.org/pdb/explore/explore.do?structureId=%s'>".replace('%s',identifier.slice(0,-1))+identifier.slice(0,-1).toLowerCase()+identifier.slice(-1)+"</a>";
	}
	else if (source=="ensp"){
		return "<a target='_blank' href='http://www.ensembl.org/id/%s'>".replace('%s', identifier) + identifier + "</a>"
	}
	else if (source=="hg38"){
		// if (position=='-'){
		formatted_identifier = identifier;
		if(identifier.split("chr").length > 1){formatted_identifier = identifier.split("chr")[1];}
		formatted_identifier = formatted_identifier.toUpperCase();
		identifier=identifier.slice(0,3).toLowerCase()+identifier.slice(3).toUpperCase();
		return "<a target='_blank' href='http://www.ncbi.nlm.nih.gov/projects/mapview/maps.cgi?taxid=9606&chr=%s'>".replace('%s', formatted_identifier) + identifier + "</a>";
		// }
		// else{return identifier}
	}
	else if (source=='reft'){
		return "<a target='_blank' href='http://www.ncbi.nlm.nih.gov/nuccore/%s'>".replace('%s',identifier.toUpperCase())+identifier.toUpperCase() + "</a>";
	}
	else if (source=='refp'){
		return "<a target='_blank' href='http://www.ncbi.nlm.nih.gov/protein/%s'>".replace('%s',identifier.toUpperCase())+identifier.toUpperCase() + "</a>";
	}
	else{
		return identifier;
	}
}


//////////////////////////////////////
//SINGLE INPUT TYPE DETECTION LOGIC//
////////////////////////////////////
var generate_random_example;

$(document).ready(function(){
	//RANDOM EXAMPLE GENERATOR
	generate_random_example=function(){
		$.get("/cgi-bin/generate.py",function(data){
			$("#inputId").val(data);
			return initiateDetection("asfd")
		})
	}
	//TYPE DETECTION LOGIC
	idtype=null;
	var geneNameProcess=null;
	var tremblSwissProcess=null;
	$('#reset_button').on("click",function(e){
		$('#inputId').trigger('mismatchEvent')
	})
	// $('#inputId').on("change",function(){alert('abcd');})
	$('#inputId').on("keyup exampleChange",function(e){return initiateDetection(e);})
	$(window).on("load",function(e){return initiateDetection(e);})
	var initiateDetection = function(e){
		$('#inputId').val();
		idtype=null;
		var input = $.trim(document.getElementById('inputId').value);
		if (geneNameProcess){geneNameProcess.abort();}
		if (tremblSwissProcess){tremblSwissProcess.abort();}

		//Error handling for cases where copy/paste, or cycling through new example
		if(e.type=="exampleChange"){
			$('#inputId').popover('destroy');
			idtype=null;
		}
		//Regex expression analysis
		
		if (input.search(/^enst[0-9]{11,11}$/i) == 0){
			idtype="Ensembl Transcript";
			$('#inputId').trigger('matchEvent');
		}
		else if (input.search(/^[0-9][a-z0-9]{3,5}$/i)==0){
			idtype = 'pdb';
			$('#inputId').trigger('matchEvent');
		}
		else if (input.search(/^[n,x]M_[0-9]{5,9}(\.[0-9]{1,2})*$/i)==0){
			idtype="Refseq Transcript";
			$('#inputId').trigger('matchEvent');
		}
		else if (input.search(/^[n,x]P_[0-9]{5,9}.*[0-9]*$/i)==0){
			idtype="Refseq Protein";
			$('#inputId').trigger('matchEvent');
		}
		else if (input.search(/^ensp[0-9]{11,11}$/i) == 0){
			idtype="Ensembl Protein";
			$('#inputId').trigger('matchEvent');
		}
		else if (input.search(/^ensg[0-9]{11,11}$/i) == 0){
			idtype="Ensembl Gene";
			$('#inputId').trigger('matchEvent');
		}

		else if (input.search(/^rs[0-9]{3,40}$/i)==0){
			idtype="dbSNP"
			$('#inputId').trigger('matchEvent');
		}
		
		else if (chrs.indexOf(input.toUpperCase())!=-1){
			idtype="Chromosome";
			$('#inputId').trigger('matchEvent');
		}
		else if (input.search(/^[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}$/i) == 0){
			tremblSwissProcess = $.get("/cgi-bin/tremblVsSwiss.cgi?uniprot="+input, function(data){
				if (data.trim()=="s"){
					idtype="SwissProt UniProt Protein";
					$('#inputId').trigger('matchEvent');
				}else if(data.trim()=="t"){
					idtype="TrEMBL UniProt Protein";
					$('#inputId').trigger('matchEvent');
				}else{
					idtype="UniProt Protein";
					$('#inputId').trigger('matchEvent');
				}
			})
		}
		else if (input.search(/^[a-z]\d\w\w\w[0-9][-][0-9]+$/i) == 0){
			idtype="Uniprot Protein Isoform";
			$('#inputId').trigger('matchEvent');
		}
		else if (input.search(/(^[1-9]$)|^([1]\d$)|^([2][0-2]$)|^[x]$|^[y]$/i)==0){
			idtype="Chromosome"; $('#inputId').trigger('matchEvent');
		}
		else if (input.search(/^[a-z]{1,1}\w*$/i) == 0){
			var geneName=null;
			geneNameProcess = $.get("/cgi-bin/ajaxGeneName.cgi?gName="+input, function(data){
				if (data.length>1){
					geneName=data;
					idtype="UniProt Reference: " +geneName;
					$('#inputId').trigger('matchEvent');
				}
			})
		}


		
		if(idtype==null){
			$('#inputId').trigger('mismatchEvent');
			
		}


		
	}

	$('#inputId').on('matchEvent', function(){
		if (idtype=="pdb"){
			if ($('#inputId').val().length>4){
				idtype="PDB Structure: " + $('#inputId').val().slice(0,4).toUpperCase() + ", " + "Chain: " + $('#inputId').val().slice(4);
			}
			else{
				idtype="PDB Structure: " + $('#inputId').val().toUpperCase();
			}
		}
		$('#inputId').popover('destroy');
		$('#inputId').popover({placement: 'top', content:idtype, trigger:'manual'});	
		$('#inputId').popover('show');
		$('#inputId').popover().attr('alive',true);
		popoverShown=true;

	})
	$('#inputId').on('mismatchEvent', function(){
		$('#inputId').popover('destroy');
		$('#inputId').popover().attr('alive',false);
		idtype=null;

	})

	// EXAMPLE CYCLING LOGIC
	var examples = ["ENST00000288602 15 CG","tp53 158 RH", "chr17 7675139 CT", "BRAF 485", "4jvgA 485 LF", "rs180177036", "P51587 31 WR","NM_000059.3 91 TA"]
	var exampleIndex = examples.length; var started=false;
	$('#exampleGenerator1').on("click", function(){
		if(exampleIndex==0){exampleIndex=examples.length;}
		exampleIndex--;
		var index = exampleIndex%examples.length
		$('#inputId').val(examples[index].split(" ")[0]).trigger("exampleChange"); $('#inputPosition').val(""); $('#inputMutation').val("");
		if(examples[index].split(" ").length>1){$('#inputPosition').val(examples[index].split(" ")[1]);}
		if(examples[index].split(" ").length>2){$('#inputMutation').val(examples[index].split(" ")[2]);}
	})
	$('#exampleGenerator2, #exampleGenerator').on("click", function(){
		if(started){exampleIndex++;}
		var index = exampleIndex%examples.length
		$('#inputId').val(examples[index].split(" ")[0]).trigger('exampleChange'); $('#inputPosition').val(""); $('#inputMutation').val("");
		if(examples[index].split(" ").length>1){$('#inputPosition').val(examples[index].split(" ")[1]);}
		if(examples[index].split(" ").length>2){$('#inputMutation').val(examples[index].split(" ")[2]);}
		started=true;
	})
})
