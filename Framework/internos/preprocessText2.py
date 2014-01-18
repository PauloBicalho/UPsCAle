#################################################################
#				 generateVectorRepresentation.py			   #
#################################################################

# -*- coding: utf-8 -*-
import getopt
import sys
import os
from dictionary2 import Dictionary2
from filters import *

MIN_WORD_LENGHT=2
MAX_WORD_LENGHT=16

def usage():
	print "\n\t\tSUPER TEXT PREPROCESSOR\n"
	print "Uso: python %s args" % sys.argv[0]
	print "args:"
	print "\t[-h]"
	print "\t-i input (texto)"
	print "\t-d dictionary"
	print "\t-v verbsDictionary"
	print "\t-o output"

def preprocess(textFile, outFile, dict, THESAURUS, CANONICA):
	fin = open(textFile, "r")
	fout = open(outFile, "w")
	
	for line in fin:
		(uid,text) = line.strip().rstrip('\n').split('\t') #alteradaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

		words = text.split(' ') #line.split
		newLine = "%s\t" % uid
		for word in words:
			if word[0].isupper():
				newLine += word + " "
			else:
				newLine += dict.getWord(word) + " "
				
		newLine = newLine.rstrip(' ')
		print >> fout, newLine
		
	fin.close()
	fout.close()


def processWord( textFile, sinsFile, verbsFile, outFile, THESAURUS, CANONICA, CORRETOR ):
	dict = Dictionary2()
	#dict.loadVerbsDictionary(verbsFile)
	#dict.loadSinDictionary(sinsFile)

	fin = open(textFile, "r")
	fout = open(outFile, "w")
	for line in fin:

		#(uid,text) = line.strip().rstrip('\n').split('\t') #alteradaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

		line = line.strip().rstrip('\n').split('\t')
		uid = line[0]
		tid = line[1]

		text = " ".join(line[2:]).strip()

		text = filter_url( text )
		text = filter_accents(text.decode('utf8', 'ignore'))
		#print text
                #text = filter_accents(unicode(text.decode('utf8')))
		text = filter_punct( text )
		text = filter_charRepetition( text ).split()

		words = [ word for word in text if word.find('@') == -1 and not word.isdigit() and len(word) > MIN_WORD_LENGHT and len(word) < MAX_WORD_LENGHT ]

		newLine = "%s\t%s\t" % ( uid, tid)
		for word in words:
			if word[0].isupper():
				newLine += word + " "
			else:
				newWord = dict.getWord(word, THESAURUS, CANONICA)
				
				if word == newWord and CORRETOR:
					newWord = correct(word)
	
					if newWord != word:
						newWord = dict.getWord(newWord, THESAURUS, CANONICA)	
					
				newLine += newWord + " "
				
		newLine = newLine.rstrip(' ')
		print >> fout, newLine.lower()
		
	fin.close()
	fout.close()
	
