#!/usr/bin/perl
use strict;
use warnings;

my $counter;
my $i;
my $index;
my $j;
my $line;
my $value;
my @values;
my $size;

my $MAX_LINES = 100;

open FIN, "<".$ARGV[0] or die "Cant open!";
### descarta primeira linha
#$line = <FIN>;

$index = 0;
$counter = 0;
while( defined($line = <FIN>) ){
     chomp($line);

     $values[$counter++] =  [ split ' ', $line ];

     if($counter == $MAX_LINES){
          open FOUT, ">".$ARGV[1]."/file".$index or die "Error!";
	  $index++;

	  $size = $#{$values[0]} + 1;
	  for($j=0;$j<$size;$j++){
	       for($i=0;$i<$counter;$i++){
		    print FOUT $values[$i][$j]," ";
	       }
	       print FOUT "\n";
	  }
	  
	  close(FOUT);
    
	 for($i=0;$i<$counter;$i++) {
		splice( @{$values[$i]} );
	 }
	  $counter = 0;

	 splice(@values);
     }

}
close(FIN);

if($counter > 0){          
	open FOUT, ">".$ARGV[1]."/file".$index or die "Error!";
	$index++;

	$size = $#{$values[0]} + 1;
	for($j=0;$j<$size;$j++){
	       for($i=0;$i<$counter;$i++){
		    print FOUT $values[$i][$j]," ";
	       }
	       print FOUT "\n";
	}
	  
	close(FOUT);
}
