#!/user/bin/perl
use strict;
use warnings;

### Declaracao de variaveis
my $numRows;
my $line;
my $numValues;
my $i;
my $columnId;
my $value;

### abre arquivo de entrada
open FIN, "<". $ARGV[0] or die "Can't open the input file $ARGV[0]!";

### abre arquivo de saida
open FOUT, ">".$ARGV[1] or die "Can't open the output file $ARGV[1]!";

$numRows = 1;

#ignora primeira linha
if( defined($line = <FIN>) ){

     while( defined($line = <FIN>) ){
	chomp($line);

	$numValues = $line;
	for($i=0; $i<$numValues; $i++){
	       if( defined($line = <FIN>) ){
		    chomp($line);
		    ($columnId,$value) = split(/ /,$line);
		    $columnId += 1;

		    print FOUT "$numRows $columnId $value\n";
	       }
	  
	}
	$numRows += 1;
		 
     }

}
close(FIN);
close(FOUT);

