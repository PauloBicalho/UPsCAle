# -*- coding: utf-8 -*-

import re
import os

MIN_NUM_OCC=3

def carrega_stopwords(language):
	file_name = 'internos/sources/StopWords/%s_stop.txt' % (language)
	file_stop = open(file_name,'r' )
	
	stop_words = set()
	for line in file_stop:
		fields = line.split('\t')
		word = fields[0]
		stop_words.add( word.lower().strip() )
	
	file_stop.close()
	
	return stop_words
	
def atualiza_log( word, valor, contador, threshold, log, stop_words):
	
	print >> log, word,

	if contador <= threshold:
		print >> log, " 1",
	if word in stop_words:
		print >> log, " 2",
	if valor <= 3:
		print >> log, " 3",
		
	print >> log, ""

def rem_stop( nome_entrada, nome_saida, valor_cortar, debug, language ):

	entrada = open(nome_entrada,'r')
	saida = open(nome_saida,'w')

	if debug == True:
		logs = '/'.join(nome_saida.split('/')[0:-1]) + '/logs/'
		command = "mkdir -p %s" % (logs)
		os.system(command)
		log = open( logs + 'stopwords(step-4).log','w')
		
		print >> log, "ARQUIVO DE LOG DA REMOCAO DE STOPWORDS\n"
		print >> log, "Legenda:"
		print >> log, "\t 1 - removida pela posicao no histograma"
		print >> log, "\t 2 - removida pela lista de stopwords"
		print >> log, "\t 3 - removida por frequencia ( <= 3 )"

	stop_words = carrega_stopwords(language)
	
	regex = r'([0-9]+)'

	r = re.compile(regex)
	threshold = int(valor_cortar)

	contador = 0
	for line in entrada:
		contador += 1

		li = line.split('\t')
		word = li[0]
		valor = int(li[1])
		
		if len(r.findall(word)) != 0 or valor <= MIN_NUM_OCC or contador <= threshold or word in stop_words:
			#atualiza_log( word, valor, contador, threshold, log, stop_words )		
			continue

		print >> saida, line.strip()
		
		
	entrada.close()
	saida.close()

	if debug == True:
		log.close()
		

