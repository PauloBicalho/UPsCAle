#!/user/bin/perl
use strict;
use warnings;

#verify the number of input parameters
die usage() if $#ARGV != 3;

### Declaracao de variaveis globais
my $scaleFactor = 100;
my $newNumTopics;

my @mapTopicDefinition;
my @mapTopicWeights;
my @percentageOfDocsPerTopic;
my @percentageOfUsersPerTopic;

my %mapNewOldTopics;
my %mergedTopics;

my $MAX_NUM_DESCRIPTORS = 15;

my $NUM_TOPICS = $ARGV[3];

#### Executa mapeamento
loadTopicDefinition();

$newNumTopics = loadTopicsMerging($NUM_TOPICS);

printTopicsInformation($newNumTopics);


sub loadTopicDefinition{
     my $definition;
     my $line;
     my $percentageOfDocs;
     my $percentageOfUsers;
     my $topicId;
     my $weight;
     my $result;
     my $i;
     my $newWeight;

     my @weights;

     open FIN, "<".$ARGV[0] or die "Can't open input file $ARGV[0]!";

     while( defined($line = <FIN>) ){
	  chomp($line);

	  ($topicId, $percentageOfDocs, $percentageOfUsers, $definition, $weight) = split(/\t/,$line);

	  $mapTopicDefinition[$topicId+1] = $definition;

	  (@weights) = split(/,/, $weight);
	  if($#weights > -1){
	  	$result =  $weights[0] * $percentageOfDocs * $scaleFactor;
		for($i=1; $i<=$#weights; $i++){
			$newWeight = $weights[$i] * $percentageOfDocs * $scaleFactor;
			$result = join(",", $result, $newWeight );
	  	}
	  }
	  else{
		$result = $weight;
	  }
	  #$mapTopicWeights[$topicId+1] = $weight;
	  $mapTopicWeights[$topicId+1] = $result;
	  $percentageOfDocsPerTopic[$topicId+1] = $percentageOfDocs;
	  $percentageOfUsersPerTopic[$topicId+1] = $percentageOfUsers;

	  splice(@weights);
     }
     close(FIN);

}



sub loadTopicsMerging{
     my $line;
     my $leavingProbability;
     my $minMergeProbability;
     my $newTopicId;
     my $numTopics;
     my $probabilityOfReach;
     my $topic1;
     my $topic2;

     ($numTopics) = @_;

     open FIN, "<".$ARGV[1] or die "Can't open input file $ARGV[1]!";

     $newTopicId = $numTopics;
     while( defined($line = <FIN>) ){
	  chomp($line);

	  ($topic1, $topic2, $probabilityOfReach, $minMergeProbability, $leavingProbability) = split(/\t/,$line);

	  $newTopicId++;
	  $mapNewOldTopics{$newTopicId}{$topic1} = 1;
	  $mapNewOldTopics{$newTopicId}{$topic2} = 1;

	  $mergedTopics{$topic1} = 1;
	  $mergedTopics{$topic2} = 1;
     }
     close(FIN);
     
     return ($newTopicId);
}

sub printTopicsInformation{
     my $component;
     my $componentId;
     my $counter;
     my $currentId;
     my $currentTopic;
     my $definition;
     my $weight;
     my $i;
     my $k;
     my $index;
     my $numLeaves;
     my $numTopics;
     my $percentageOfDocs;
     my $percentageOfUsers;
     my $topicId;
     my $trash1;
     my $topDescriptors;
     my $topWeights;

     my @components;
     my @leafNodes;
     my @currentLeaves;
     my @trash2;

     my %children;
     my %mapComponentLevel;
     my %mapComponentId;
     

     ($numTopics) = @_;

     open FOUT, ">".$ARGV[2] or die "Can't open output file $ARGV[2]!";

     #imprime hierarquia de topicos usando busca em largura
     for($topicId=1; $topicId<=$numTopics; $topicId++){

	  #é um nodo do nivel 1
	  if( !exists($mergedTopics{$topicId}) ){

	       #encontra componentes deste topico

	       $index = 0;
	       $numLeaves = 0;
	       $components[$index] = $topicId;
	       $mapComponentLevel{$topicId} = 0;
	       $mapComponentId{$topicId} = sprintf(";%d;",$index);

	       #alcança em largura os filhos 
	       for($i=0; $i<=$index; $i++){

		    $k = 0;
		    $children{$components[$i]}[$k++] = $components[$i];
		    foreach $component ( sort {$a <=> $b} (keys(%{$mapNewOldTopics{$components[$i]}}) ) ) {  
			 $components[++$index] = $component;
			 $mapComponentLevel{$component} = $mapComponentLevel{$components[$i]} + 1;
			 $children{$components[$i]}[$k++] = $component;
			 $mapComponentId{$component} = sprintf(";%d%s",$index,$mapComponentId{$components[$i]});
		    }
	  
	       }
	       $index--;

	       #imprime filhos do nodo raiz
	       foreach $component (@components){
		    $counter = 0;
		    
		    if( $component <= $NUM_TOPICS ){
			      $definition = $mapTopicDefinition[$component];
			      $weight = $mapTopicWeights[$component];
			      $percentageOfDocs = $percentageOfDocsPerTopic[$component];
			      $percentageOfUsers = $percentageOfUsersPerTopic[$component];     
			      $currentLeaves[$counter++] = $component;
		    }
		    else{
			 $definition = "";
			 $weight = "";
			 $percentageOfDocs = $percentageOfUsers = 0;
			 ($trash1,$componentId,@trash2) = split(/;/,$mapComponentId{$component});
			 foreach $currentTopic ( keys(%mapComponentId) ){
			      $currentId = $mapComponentId{$currentTopic};
			      if( ($currentTopic < $NUM_TOPICS) && ($currentId =~ /;$componentId;/)){
				  if( $definition eq "" ){
					  $definition =  $mapTopicDefinition[$currentTopic];
					  $weight =  $mapTopicWeights[$currentTopic];
				  }
				  else{
					  $definition = join(",", $definition, $mapTopicDefinition[$currentTopic]);
					  $weight = join(",", $weight, $mapTopicWeights[$currentTopic]);
				  }			      
				  $currentLeaves[$counter++] = $currentTopic;
				  $percentageOfDocs += $percentageOfDocsPerTopic[$currentTopic];
				  $percentageOfUsers += $percentageOfUsersPerTopic[$currentTopic];
			      }
			 }
			 splice(@trash2);
		    }

		    ($topDescriptors, $topWeights) = getClusterDefinition($definition, $weight);
		    print FOUT $mapComponentLevel{$component},"\t",$component,"\t",join(",",@{$children{$component}}),"\t",join(",",@currentLeaves),"\t",$percentageOfDocs,"\t",$percentageOfUsers,"\t",$topDescriptors,"\t",$topWeights,"\n";

		    splice(@currentLeaves);
	       }
	  }

	  splice(@components);
	  splice(@leafNodes);

	  %children = ();
	  %mapComponentLevel = ();
	  %mapComponentId = ();

     }

     close(FOUT);
}

sub getClusterDefinition{
	my $definition;
	my $i;
	my $word;
	my $numWords;
	my $result;
	my $result1;
	my $weight;

	my @words;
	my @weights;

	my %hashOfWords = ();

	($definition, $weight) = @_;

	(@words) = split(/,/,$definition);
	(@weights) = split(/,/,$weight);

	$numWords = $#words + 1;
	for($i=0;$i<$numWords;$i++){
		if( exists($hashOfWords{$words[$i]}) ){
			$hashOfWords{$words[$i]} += $weights[$i];
			#$hashOfWords{$words[$i]} += log(1 + $weights[$i]);
		}
		else{
			$hashOfWords{$words[$i]} = $weights[$i];
			#$hashOfWords{$words[$i]} = log(1 + $weights[$i]);
		}
	}

	$numWords = 0;
	foreach $word ( sort {$hashOfWords{$b} <=> $hashOfWords{$a} } keys(%hashOfWords) ){
		if($numWords == $MAX_NUM_DESCRIPTORS){
			last;
		}

		if($numWords == 0){
			$result = $word;
			$result1 = $hashOfWords{$word};
		}
		else{
			$result = join(",",$result,$word);
			$result1 = join(",",$result1,$hashOfWords{$word});
		}
		$numWords++;
	}

	splice(@words);
	return($result, $result1);
}

sub usage{
	print "\nIn order to run this script you should give 4 input parameters:\n";
	print " \tInput file name containing the topic information\n";
	print " \tInput file name containing the topic merging schema\n";
	print " \tOutput file name \n";
	print " \tNum topics od the domain\n\n";
}
