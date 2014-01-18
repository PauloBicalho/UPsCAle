#!/usr/bin/perl
use strict;
use warnings;

my $index;
my $line;
my @eigenValues;
my @row;
my $value;

open S_MATRIX, "<".$ARGV[0] or die "Can't open the file $ARGV[0]!";

$index = 0;
$line = <S_MATRIX>;
while( defined($line = <S_MATRIX>) ){
     chomp($line);

     $eigenValues[$index++] = $line;
}
close(S_MATRIX);


open V_MATRIX, "<".$ARGV[1] or die "Can't open the file $ARGV[1]!";
open R_MATRIX, ">".$ARGV[2] or die "Can't open the file $ARGV[2]!";

$index = 0;
$line = <V_MATRIX>;
while( defined($line = <V_MATRIX>) ){
     chomp($line);

     (@row) = split(/ /,$line);

     foreach $value (@row){
	  print R_MATRIX $value*$eigenValues[$index], " "; 
     }
     print R_MATRIX "\n";

     splice(@row);
     $index++;
     if( !(defined($eigenValues[$index])) ){	
	  last;	
     }
}
close(V_MATRIX);
close(R_MATRIX);
