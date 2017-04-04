#!/usr/bin/perl


# read from command-line
$inFastaFile  = $ARGV[0];

# open files
open(fastaFile , "<$inFastaFile")  || die "File not found - \"Fasta File\"!\n";



# read fasta sequences (main file)
# boolean parameters
$newSeq   = 0;
$startSeq = 0;

# count entries
$arrCount = -1;

while(<fastaFile>){
  chomp($_);
	
	if($startSeq && !($_ eq "") && !($_ =~ m/^>/)){
		$seqArr[$arrCount][1] = $seqArr[$arrCount][1] . $_;
	}
	
	if($newSeq && !($_ eq "")){
		$seqArr[$arrCount][1] = $_;  		
  		$newSeq   = 0;
  		$startSeq = 1;
	}
	
	if($_ =~ m/^>/){
		$arrCount = $arrCount + 1;
		$seqArr[$arrCount][0] = $_; 
		$newSeq   = 1;
		$startSeq = 0;
	}
}
close(fastaFile);


#------------------------------------------------------------
# Store sequence in hash as key value. 
# It is necessary to compare READS
%noDoubles = ();
%test      = ();

for($i = 0 ; $i <  $#seqArr+1 ; $i++ ){
	if(exists $noDoubles{$seqArr[$i][1]}){
		$noDoubles{$seqArr[$i][1]}[1] += 1;	
	 	$test{$noDoubles{$seqArr[$i][1]}[0]} .= ";" . $seqArr[$i][0];
	}else{
		# $idName is Hash-Key
		$idCountData[0] = $seqArr[$i][0];
		$idCountData[1] = 1;
		@{ $noDoubles{$seqArr[$i][1]} } =  @idCountData;
		$test{$seqArr[$i][0]} = $seqArr[$i][0];
	}
}



#----------------------------------------------
# SAVE RESULT IN TWO FILES
# File 1 : Fasta File
# File 2 : ID and the number of same reads
@name = split('\.',$inFastaFile);
$tmpFileName = "autoGen" . "-" . $name[0] . ".fasta";
open(FILE , ">$tmpFileName")  || die "File can't be written - \"Fasta File\"!\n";
	while ( ($k,$v) = each %noDoubles ) {
		$tmp = $noDoubles{$k}[0] . " weight|" . $noDoubles{$k}[1] . "\n" . $k . "\n";
		print FILE $tmp; 
	}
close(FILE);


$tmpFileName = "autoGen" . "-" . $name[0] . ".icn";
open(FILE , ">$tmpFileName")  || die "File can't be written - \"Cluster File\"!\n";
	while ( ($k,$v) = each %test ) {
		$tmp =  $k . "\t" . $v . "\n";
		print FILE $tmp; 
	}
close(FILE);
