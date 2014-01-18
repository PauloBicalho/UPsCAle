#################################################################
#					   dictionary.py							#
#################################################################

# -*- coding: utf-8 -*-
import sys
from flexWords import flexWords


class Dictionary2:
	def __init__(self):
		self.verbs = {}		 # verbos conjulgados => verbo no infinitivo
		self.sins = {}		  # sinonimo => palavra
		
	
	def loadVerbsDictionary(self, fileName):
		file = open(fileName, "r")
		for line in file:
			verbs = line.split()
			for verb in verbs:
				verb = verb.rstrip('\n')
				self.verbs[verb] = verbs[0]
		file.close
		self.lastId = id
	

	def printVerbsDictionary(self):
		for verb in self.verbs:
			print verb, self.verbs[verb]


	def loadSinDictionary(self, fileName):
		file = open(fileName, "r")
		while(True):
			line = file.readline()
			if not line: break
			(word,numSin) = line.split('|')
			self.sins[word] = word
			while(int(numSin) > 0):
				line = file.readline()
				if not line: break
				sins = line.split('|')
				# insere no hash
				for sin in sins:
					sin = sin.rstrip('\n')
					self.sins[sin] = word
				numSin = int(numSin)-1
		file.close()


	def loadSinDictionary2(self, fileName):
		file = open(fileName, "r")
		while(True):
			line = file.readline()
			if not line: break
			(word,numSin) = line.split('|')
			while(int(numSin) > 0):
				line = file.readline()
				if not line: break
				sins = line.split('|')
				# insere no hash
				for sin in sins:
					sin = sin.rstrip('\n')
					if sin not in self.sins:
						self.sins[sin] = True
				numSin = int(numSin)-1
		file.close()


	def printSinsDictionary(self):
		for word in self.sins:
			print word, self.sins[word]


	def getWord(self, word, THESAURUS, CANONICA):
		
		#if THESAURUS == True and word in self.sins:
		if CANONICA == True and word in self.verbs:
			
			if THESAURUS == True and self.verbs[word] in self.sins:
				return self.sins[self.verbs[word]]
			else:
				return self.verbs[word]
			
		elif THESAURUS == True and word in self.sins:
			return self.sins[word]
			
		else:
			newWord = flexWords(word)
			#return newWord
			if CANONICA == True and newWord in self.verbs:
			
				if THESAURUS == True and self.verbs[newWord] in self.sins:
					return self.sins[self.verbs[newWord]]
				else:
					return self.verbs[newWord]
			
			elif THESAURUS == True and newWord in self.sins:
				return self.sins[newWord]
				
			#return newWord
			return word

