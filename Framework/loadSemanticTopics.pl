#!/usr/bin/perl
use strict;
use warnings;
use DBD::mysql;
use utf8;

my $dbh;

my %hashOfDescription;
my %hashOfDefinition;

#verify the number of input parameters
die usage() if $#ARGV != 9;

my $START_TIME = $ARGV[0];

my $END_TIME = $ARGV[1];

open TOPIC_INFO, "<".$ARGV[2] or die "Can't open the input file $ARGV[2]";

open TOP_TERMS, "<".$ARGV[3] or die "Can't open the input file $ARGV[3]";

open TOP_DOCS, "<".$ARGV[4] or die "Can't open the input file $ARGV[4]";

#get name of the output table
my $OUT_TABLE = $ARGV[5];
 
configureMySQLConnection($ARGV[6],$ARGV[7],$ARGV[8],$ARGV[9]);

loadTopicDescription();

loadTopicDefinition();

loadTopicInfo();

#initial configuration of mysql
sub configureMySQLConnection{
	# Mysql information
	my $database;
	my $host;
	my $userid;
	my $passwd;
	my $connection;

	($database,$host,$userid,$passwd) = @_;	

	$connection = "dbi:mysql:$database:$host";

	# Make connection to database
	$dbh = DBI->connect($connection,$userid,$passwd);
	$dbh->{'mysql_enable_utf8'} = 1;
	$dbh->do('SET NAMES utf8');
}

sub loadTopicDescription{
     my $line;
     my $topicId;
     my $remain;

     while( defined($line = <TOP_TERMS>) ){
	  chomp($line);

	  ($topicId, $remain) = split(/\t/, $line);
	  $hashOfDescription{$topicId} = $remain;
     }
     close(TOP_TERMS);
}

sub loadTopicDefinition{
     my $line;
     my $topicId;
     my $remain;

     while( defined($line = <TOP_DOCS>) ){
	  chomp($line);

	  ($topicId, $remain) = split(/\t/, $line);
	  $hashOfDefinition{$topicId} = $remain;
     }
     close(TOP_DOCS);
}

sub loadTopicInfo{
     my $line;
     my $level;
     my $id;
     my $children;
     my $leaves;
     my $docWeight;
     my $userWeight;
     my $definition;
     my $query;
     my $sth;
 
     while( defined($line = <TOPIC_INFO>) ){
	  chomp($line);

	  ($level, $id, $children, $leaves, $docWeight, $userWeight, $definition) = split(/\t/, $line);

	  $query = "INSERT IGNORE INTO $OUT_TABLE VALUES ('$START_TIME', '$END_TIME', '$id', '$level', '$docWeight', '$userWeight', '$children', '$leaves', '".$hashOfDescription{$id}."', '".$hashOfDefinition{$id}."');";
     
	  $sth = $dbh->prepare($query);
	  $sth->execute();
     }
     close(TOPIC_INFO);
}

sub usage{
	print "\nIn order to run this script you should give 10 input parameters:\n";
	print " \tstart Time Name \n";
	print " \tend Time \n";
	print " \tTopic Info File Name \n";
	print " \tTop Terms File Name \n";
	print " \tTop Documents File Name \n";	
	print " \tOutput table's name \n";
	print " \tMysql database name \n";
	print " \tMysql host name \n";
	print " \tMysql user name \n";
	print " \tMysql password \n\n";
}


