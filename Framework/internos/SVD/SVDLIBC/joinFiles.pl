#!/usr/bin/perl
use strict;
use warnings;

my $file;
my $i;
my $j;
my $line;

my @inFile;

my $NUM_FILE= $ARGV[2];

open FOUT, ">".$ARGV[1] or die "Error!";

for($i=0;$i<$NUM_FILE;$i++){
     open $inFile[$i], "<".$ARGV[0]."/file".$i or die "Cant open!";
}

for($j=0;$j<3000000;$j++){

     foreach $file (@inFile){
	  if( defined($line = <$file>) ){
	       chomp($line);

	       print FOUT "$line ";
	  }
	  else{
	       print "$j\n";
	       close(FOUT);
	       exit;
	  }
     }
     print FOUT "\n";

}
