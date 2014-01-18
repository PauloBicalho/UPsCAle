#!/usr/bin/perl
use strict;
use warnings;

### Declaracao de variaveis
my $numTerms;
my $line;
my $rank;
my $frequency;
my $term;
my $k;
my $second_norm;

my @sigma;
my @sigma_norm;
my @second_derivative;
my $i;

# verify the number of input parameters
die usage() if $#ARGV != 1;

open FIN, "<".$ARGV[0] or die "Can't open the file $ARGV[0]!";

my $PRECISION = $ARGV[1];

#load input data
$numTerms = 0;
while( defined($line = <FIN>) ){
    chomp($line);

    ($term,$frequency) = split(/\t/,$line);
    $sigma[$numTerms++] = $frequency;
}
$k = $numTerms;
close(FIN);

$second_norm = $sigma[1];
for($i=0; $i<$k; $i++){
    $sigma_norm[$i]  = $sigma[$i] / $second_norm;
    $second_derivative[$i] = 0;
}

#curve approximating the second derivative 
for($i=1; $i<($k-1); $i++){
  $second_derivative[$i] = $sigma_norm[$i-1] - 2*$sigma_norm[$i] + $sigma_norm[$i+1];
}

#search rank
$rank = $k - 1;
while ($rank > 1){ 
    $rank = $rank - 1;
    if (abs($second_derivative[$rank]) >= $PRECISION){
	last;
    }
} 

print $rank;


sub usage{
        print "\nIn order to run this script you should give 2 input parameters:\n";
        print " \tInput file name \n";
        print " \tMinimum precision for second derivate \n\n";
}
