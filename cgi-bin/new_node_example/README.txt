NEW NODE TUTORIAL
This is a tutorial on how you, the user, can add a new identifier and connect it to an existing
identifier. There are four different classes of identifiers: chromosome, gene, transcript, protein.
To add a new identifier, you must supply certain info and data files, depending on the class of the
identifier. 

	Chromosome:
		Required info:
			-Input class--class of the identifier you are inserting
			-Output class--class of the identifier you are connecting your new identifier to
			-Input id type--The name of your new identifier. For example, if you are inserting uniprot
			into the existing graph, you would most likely call the identifier "uniprot". The input
			id type is what you will input into the -t (--type) option in the command line.
			-Output id type--The name of the existing identifier you are connecting your new identifier
			to
		Required data files:
			-A .txt file which maps your new identifier directly to your old identifier. For example,
			if the new identifier is enst and the old identifier is uniprot, one line in your .txt file
			may appear as follows:
				ENST00000253159	Q9UL36
			Notice that the input and output are separated by a single tab. This will be explained in more
			detail later.
			-A .txt file which maps your new identifier directly to its sequence. 


	Gene:
		Required info:
			*Same as above*
		Required data files:
			-A .txt file which maps your new identifier directly to your old identifier
			-A .txt file which maps your new identifier directly to its sequence.
			-A .txt file which maps your new identifier directly to its start and end positions on its chromosome.

	Transcript:
		Required info:
			*Same as above*
		Required data files:
			-A .txt file which maps your new identifier directly to your old identifier
			-A .txt file which maps your new identifier directly to the sign of its strand followed by its sequence
			-A .txt file which maps your new identifier to its positions on its corresponding chromosome

	Protein:
		Required info:
			*Same as above*
		Required data files:
			-A .txt file which maps your new identifier directly to your old identifier
			-A .txt file which maps your new identifier directly to its amino acid sequence	



	Data file structure:
		The exact structure of the .txt data files is important, and this section will go into this more thoroughy. After this 
		section, make sure to look at the examples data files in this directory.

		I: New identifier -> old identifier (for all classes)
		newId1	oldId1
		newId2	oldId2
		newId3	oldId3

		II: New identifier -> sequence (for all classes except transcript)
		newId1	sequence1
		newId2	sequence2
		newId3	sequence3

		III: New identifier -> sign (+ or -) -> sequence (for transcript only)
		newId1 sign1 sequence1
		newId2 sign2 sequence2
		newId3 sign3 sequence3

		IV: New identifier -> chromosome start position -> chromosome end position (for gene only)
		newId1 startpos1 endpos1
		newId2 startpos2 endpos2
		newId3 startpos3 endpos3

		V: New identifier -> coding start position -> coding end position -> exon start positions -> exon end positions
		newId1	cds1	cde1	esp1,esp2,esp3,esp4	ese1,ese2,ese3,ese4
		newId2	cds2	cde2	esp5,esp6,esp7,esp8	ese5,ese6,ese7,ese8


		NOTE: Remember, these .txt files are tab-delimited; each entry should be separated by a single tab

	Template:
		Now that you have your data files and information, the program needs to know how to access these data files and info.
		This is achieved through the use of a template. The template should be a .txt file in the following format:

		input_class: X
		output_class: X
		input_id_type: X
		output_id_type: X
		inputToOutput: X
		inputToSequence: X
		inputToPosition: X


		The X's should be filled in with your information. The first four fields are self-explanatory. THe inputToOutput field should be the directory of your .txt file mapping your new identifier to your old identifier (I). inputToSequence should be the 
		directory of your .txt file mapping your new identifier to its sequence (and possibly sign)--II or III. Finally, inputToPosition should be the directory of your .txt file mapping your new identifier to its position(s) along the chromosome
		(IV or V). NOTE: What you fill in for X should NOT be in quotes or ''.


	Example:
		Now you will be given an opportunity to add an example identifier whose data files have already been provided. The template is located in this directory and is titled 'template.txt'. Feel free to look at it to gain an understanding of what a valid template looks like. Also, it is recommended that you take a look at the data files which the template refers to as well to understand the importance of a tab-delimited structure for your .txt data files. Instructions on how to add the new identifier (the example template outlines a new identifier called 'refp'. This is a refSeq protein identifier from the refSeq database.) are as follows:

		COMMAND LINE
		************
		1. Open terminal
		2. Cd into toUniProt's root directory
		3. Enter "python config.py -n "
		4. Drag and drop your template file into the terminal window
		5. Hit enter

		IMPORTABLE MODULE
		***************** 
		1. Open terminal.
		2. Cd into the projects root directory.
		3. Enter the python command line.
		4. Import pipeFactory.
		5. Execute pipeFactory's function buildPipe(X)
			-To do this, simple type pipeFactory.buildPipe(X), where X is the directory to the example template. If you ever made your own template, this would be the directory to your template.
		6. Hit enter, and buildPipe will fully incorporate your new node into the graph!
			-To achieve this, it adds the new identifier to an identifier graph, which represents all the connections between all identifiers. Then it uses your data files to create mySQL tables. Finally, it creates both an input to output, and an output to input, pipe, allowing bidirectional traversal between your new identifier and the existing identifier you connected to.















