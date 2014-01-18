# -*- coding: utf-8 -*-
import operator
import sys
import os
import commands

sys.path.append('internos/')

from preprocessText2 import processWord
from Stopwords import rem_stop
from Tecnica import *

def criar_histograma( nome_entrada, nome_saida ):
	
	entrada = open(nome_entrada,'r')
	saida = open(nome_saida,'w')

	palavras = {}

	for line in entrada:

		line = line.split('\t')
		if len(line) < 3:
			continue;
		tweet_id = line[0]

		words = line[2].lower().split()
		
		for word in words:
			if word not in palavras:
				palavras[word] = 0
			palavras[word] += 1	

	sorted_hist = sorted(palavras.iteritems(), key=operator.itemgetter(1), reverse = True)
		
	for palavra,valor in sorted_hist:
		print >> saida, "%s\t%s" % (palavra,valor)

	entrada.close()
	saida.close()

	return nome_saida
	
	
def remover_duplicatas( arquivo_entrada, arquivo_saida ):
	
	comando = "sort -u -k 3 %s -o %s" % (arquivo_entrada, arquivo_saida)
	
	os.system(comando)

	return arquivo_saida

def preprocessar_texto( arquivo_entrada, arquivo_saida ):
		
	arquivo_thesaurus = 'internos/sources/thesauroPT.dat'
	arquivo_verbs = 'internos/sources/verbsDictionary.txt'

	processWord( arquivo_entrada, arquivo_thesaurus, arquivo_verbs, arquivo_saida, False, True, False )

	# ./stemwords [-l <language>] [-i <input file>] [-o <output file>] 

	return arquivo_saida

#primeiro parametros: arquivo de saida do histograma
def remover_stopwords( arquivo_entrada, arquivo_saida, language ):

	saida =  '/'.join( arquivo_saida.split('/')[:-1] ) + '/dimen'

	cmd = "perl internos/selectCutPoint.pl %s 0.001 > %s" % (arquivo_entrada,saida)
	os.system( cmd )

	df = open( saida, 'r' )
	threshold = int ( df.readline().strip() )
	df.close()

	if threshold > 1000:
		threshold = 100;
	print "----Cut Point: %s" % threshold
	
	rem_stop( arquivo_entrada, arquivo_saida, threshold, False, language )

	return arquivo_saida
	
def agrupar_texto( arquivo_entrada, arquivo_saida ):
	entrada = open( arquivo_entrada, 'r' )
	saida = open( arquivo_saida, 'w' )
	
	texto = {}
	for line in entrada:
		line = line.strip().split('\t')
		
		id_texto = line[0]
		
		if id_texto not in texto:
			texto[ id_texto ] = []
			
		texto[ id_texto ].append( line[2] )
	
	entrada.close()
		
	contador = 0
	for id_texto in texto:
		print >> saida, "%s\t%s\t%s"  % (id_texto, contador, " ".join( texto[ id_texto ] ) )
		contador += 1
		
	saida.close()
	
	return arquivo_saida

