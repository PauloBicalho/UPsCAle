#!/usr/bin/perl
use strict;
use warnings;

### Declaracao de variaveis globais
my %hashOfTopics;

# Abre arquivo de saida
open FOUT, ">>".$ARGV[2] or die "Can't open the output file $ARGV[2]!";

loadTopItems();

close(FOUT);

sub loadTopItems{
    my $line;
    my $topicId;
    my $remain;
    my $item;
    my $position;

    my @topItems;

    open FIN1, "<".$ARGV[0] or die "Can't open the input file $ARGV[0]!";

    while( defined($line = <FIN1>) ){
	  chomp($line);

	  ($topicId, $remain) = split(/\t/,$line);
	  (@topItems) = split(/ /, $remain);

	  $position = 1;
	  foreach $item (@topItems){
		$hashOfTopics{$topicId}{$item} = $position++;
	  }

	  mapItems($topicId);

	  splice(@topItems);
    }
    close(FIN1);
}

sub mapItems{
    my $topicId;
    my $line;
    my $item;

    my @data;

    my %hashOfItems;

    ($topicId) = @_;

    open FIN2, "<".$ARGV[1] or die "Can't open the input file $ARGV[1]!";

    while( defined($line = <FIN2>) ){
	  chomp($line);

	  (@data) = split(/ /, $line);

	  if( exists($hashOfTopics{$topicId}{$data[1]}) ){
	      $hashOfItems{$hashOfTopics{$topicId}{$data[1]}} = $data[3];
	  }

	  splice(@data);
    }
    close(FIN2);

    print FOUT $topicId, "\t";
    foreach $item ( sort {$a <=> $b} (keys(%hashOfItems)) ){
	  print FOUT $hashOfItems{$item}, " ";
    }
    print FOUT "\n";

    %hashOfItems = ();

}

