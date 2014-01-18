#!/usr/bin/perl
use strict;
use warnings;

### Declaracao de variaveis globais
my $firstColumn;
my $i;
my $line;
my $numNonZeros;
my $columnIndex;
my $value;

my %hashOfColumns;

### Abre arquivo de entrada
open FIN, "<". $ARGV[0] or die "Can't open the input file $ARGV[0]!";

### Abre arquivo de saida
open FOUT, ">". $ARGV[1] or die "Can't open the output file $ARGV[1]!";

#ignora primeira linha
if(defined($line = <FIN>) ){
     while( defined($line = <FIN>) ){
	  chomp($line);

	  $numNonZeros = $line;

	  for($i=0; $i<$numNonZeros; $i++){
	       if( defined($line = <FIN>) ){
		    chomp($line);
	       
		    ($columnIndex,$value) = split(/ /,$line);

		    $hashOfColumns{$columnIndex} = $value;
	       }
	       else{
		    print "\t***Error: not syncronized file!\n\n";
		    exit;
	       }
	  }

	  $firstColumn = 1;
	  foreach $columnIndex (sort {$a <=> $b} keys(%hashOfColumns)  ){
	       if( $firstColumn == 1 ){
		    print FOUT $columnIndex, ":", $hashOfColumns{$columnIndex};
		    $firstColumn = 0;
	       }
	       else{
		    print FOUT " ", $columnIndex, ":", $hashOfColumns{$columnIndex};
	       }
	  }
	  print FOUT "\n";

	  %hashOfColumns = ();
     }
}
close(FIN);
close(FOUT);
