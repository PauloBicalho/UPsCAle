#!/usr/bin/perl
use strict;
use warnings;

### Declaracao de variaveis glovais
my $scaleFactor = 100;

my %hashOfDocsPerTopic;
my %topicsWeight;

#verify the number of input parameters
die usage() if $#ARGV != 4;

open TOPICS_PER_DOC, "<".$ARGV[0] or die "Can't open the input file $ARGV[0]!";

open TOPIC_INFO, "<".$ARGV[1] or die "Can't open the input file $ARGV[1]!";

open TOPICS_RELEVANCE, "<".$ARGV[2] or die "Can't open the input file $ARGV[2]!";

open FOUT, ">".$ARGV[3] or die "Can't open the output file $ARGV[3]!";

my $MAX_ITEMS = $ARGV[4];

loadDocsPerTopic();
loadTopicsRelevance();
loadTopicsHierarchy();

sub loadDocsPerTopic{
	my $line;
	my $docId;
	my $text;
	my $topic;
	my $topicId;
	my $weight;
	my $topicList;

	my @topics;

	while( defined($line = <TOPICS_PER_DOC>) ){
		chomp($line);

		($docId, $text, $topicList) = split(/\t/, $line);

		$topicList =~ s/^ //g; 
		$topicList =~ s/[ ][ ]*/ /g; 
		(@topics) = split(/ /, $topicList);
		foreach $topic (@topics){
			($topicId, $weight) = split(/=/, $topic);
			$hashOfDocsPerTopic{$topicId}{$docId} = $weight;
		}
		splice(@topics);
	}
	close(TOPICS_PER_DOC);
}

sub loadTopicsRelevance{
	my $line;
	my $topicId;
	my $docWeight;
	my $userWeight;
	
	my @remain;

	while( defined($line = <TOPICS_RELEVANCE>) ){
		chomp($line);

		($topicId, $docWeight, $userWeight, @remain) = split(/\t/, $line);

		$topicsWeight{$topicId} = $docWeight;
	}
	close(TOPICS_RELEVANCE);
}

sub loadTopicsHierarchy{
     my $line;
     my $level;
     my $id;
     my $children;
     my $leaves;
     my $docWeight;
     my $userWeight;
     my $definition;
     my $weights;
 
     while( defined($line = <TOPIC_INFO>) ){
	  chomp($line);

	  ($level, $id, $children, $leaves, $docWeight, $userWeight, $definition, $weights) = split(/\t/, $line);

    	  print FOUT $id, "\t", retrieveRelevantDocuments($leaves), "\n";
     }
     close(TOPIC_INFO);
     close(FOUT);
}

sub retrieveRelevantDocuments{
        my $topicList;
	my $numDocs;
	my $topic;
	my $doc;
	my $index;
	my $maxNumDocs;
	my $result = "";

	my @sortedWeights;
        my @topics;

        my %hashOfDocs = ();

        ($topicList) = @_;

        (@topics) = split(/,/,$topicList);

	foreach $topic ( @topics ){
		$topic = $topic - 1;
		foreach $doc ( keys( %{$hashOfDocsPerTopic{$topic}}) ){
			if( exists($hashOfDocs{$doc}) ){
				$hashOfDocs{$doc} += $hashOfDocsPerTopic{$topic}{$doc};
				#$hashOfDocs{$doc} += $hashOfDocsPerTopic{$topic}{$doc} * $topicsWeight{$topic} * $scaleFactor;
				#$hashOfDocs{$doc} += log(1.0 + $hashOfDocsPerTopic{$topic}{$doc});
			}
			else{
				$hashOfDocs{$doc} = $hashOfDocsPerTopic{$topic}{$doc};
				#$hashOfDocs{$doc} = $hashOfDocsPerTopic{$topic}{$doc} * $topicsWeight{$topic} * $scaleFactor;
				#$hashOfDocs{$doc} = log(1.0 + $hashOfDocsPerTopic{$topic}{$doc});
			}
		}
	}

	$index = 0;
        foreach $doc ( sort {$hashOfDocs{$b} <=> $hashOfDocs{$a} } keys(%hashOfDocs) ){
		$sortedWeights[$index++] = $hashOfDocs{$doc};
	}
#	$maxNumDocs = getCutPoint($index, $PRECISION, @sortedWeights);
	$maxNumDocs = $MAX_ITEMS;

        $numDocs = 0;
        foreach $doc ( sort {$hashOfDocs{$b} <=> $hashOfDocs{$a} } keys(%hashOfDocs) ){
                if($numDocs == $maxNumDocs){
                        last;
                }

                if($numDocs == 0){
                        $result = $doc;
                }
                else{
                        $result = join(",",$result,$doc);
                }
                $numDocs++;
        }

        splice(@topics);
	splice(@sortedWeights);
        return($result);
}

sub getCutPoint{
	my $num_items;
	my $precision;
	my $second_norm;
	my $rank;
	my $i;

	my @sigma;
	my @sigma_norm;
	my @second_derivative;

	($num_items, $precision, @sigma) = @_;

        @sigma_norm = ();
        @second_derivative = ();

        $second_norm = $sigma[1];
        for( $i=0; $i<$num_items; $i++){
                $sigma_norm[$i]  = $sigma[$i] / $second_norm;
                $second_derivative[$i] = 0;
	}

        #curve approximating the second derivative 
        for( $i=1; $i<($num_items-1); $i++){
                $second_derivative[$i] = $sigma_norm[$i-1] - 2*$sigma_norm[$i] + $sigma_norm[$i+1];
	}

        #search rank
        $rank = $num_items - 1;
        while ($rank > 1){
                $rank = $rank - 1;
                if ( abs($second_derivative[$rank]) >= $precision) {
                        last;
		}
	}

        return ($rank);
}

sub usage{
	print "\nIn order to run this script you should give 5 input parameters:\n";
	print " \tTopics per document file name \n";
	print " \tTopics hierarchy file name \n";
	print " \tTopics relevance file name \n";
	print " \tOutput file name \n";
	print " \tMaximum number of documents por topic \n\n";	
}
