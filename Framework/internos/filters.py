#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import string
import unicodedata


stopwords = set( ["vc","oque","ta","de","a","o","que","e","do","da","em","um","para","e","com","nao","uma","os","no","se","na","por","mais","as","dos","como","mas","foi","ao","ele","das","tem","a","seu","sua","ou","ser","tbm","tbem","quando","muito","ha","nos","ja","esta","eu","tambem","so","pelo","nele","pela","ate","isso","ela","entre","era","depois","sem","mesmo","aos","ter","seus","quem","nas","me","esse","eles","estao","voce","tinha","foram","essa","num","nem","suas","meu","as","minha","tem","numa","pelos","elas","havia","seja","qual","sera","nos","tenho","lhe","deles","essas","esses","pelas","este","fosse","dele","tu","te","voces","vos","lhes","meus","minhas","teu","tua","teus","tuas","nosso","nossa","nossos","nossas","dela","delas","esta","estes","estas","aquele","aquela","aqueles","aquelas","isto","aquilo","estou","daqui","esta","estamos","estao","estive","esteve","estivemos","estiveram","estava","estavamos","estavam","estivera","estiveramos","esteja","estejamos","estejam","estivesse","estivessemos","estivessem","estiver","estivermos","estiverem","hei","ha","havemos","hao","houve","houvemos","houveram","houvera","houveramos","haja","hajamos","hajam","houvesse","houvessemos","houvessem","houver","houvermos","houverem","houverei","houvera","houveremos","houverao","houveria","houveriamos","houveriam","sou","fico","somos","sao","era","eramos","eram","fui","foi","fomos","foram","fora","foramos","seja","sejamos","sejam","fosse","fossemos","fossem","for","formos","forem","serei","sera","seremos","serao","seria","seriamos","seriam","tenho","tem","temos","haver","tinha","tinhamos","tinham","tive","teve","tivemos","tiveram","tivera","tiveramos","tenha","tenhamos","tenham","tivesse","tivessemos","tivessem","tiver","tivermos","tiverem","terei","tera","teremos","terao","teria","teriamos","teriam","todo","toda","cada","muitos","muita","muitas","pouco","pouca","poucos","poucas","apenas","ainda","assim","vim","vcs","logo","entao","apos","aqui","antes","fato","onde","debaixo","acima","embaixo","ali","ala","pode","puderam","pude","net","http","mail","hora","alguem","vou","fale","quais","qual","nunca","sairam","todos","todo","melhor","desde","disse","www","webmail","vai","deve","uso","todas","alem","outras","maior","ir","vir","mim","profile","sites","fazer","partir","sobre","local","menos","maioria","sempre","desses","minimo","vai","quanto","pois","are","porque","aumentar","site","diz","vez","bem","dois","tres","quatro","cinco","seis","sete","oito","nove","dez","agora","mail","estar","groupurl","groups","hoje","deste","sob","afirmar","outra","tanto","tal","ultima","primeira","poder","encontrar","sendo","nova","explica","outros","duas","alta","novos","desse","atuar","segundo","neste","nesta","nisto","desta","dessa","disso","porem","alguns","algumas","umas","algum","mesma","outro","ontem","proxima","nenhum","quaisquer","qualquer","feira","visto","dizer","etc","nenhuma","demais","sido","podem","vao","feiras","nesse","dar","via","alo","usar","ola","tai","dia","dias","ano","anos","portanto","todavia","nada","tudo","quase","durante","comigo","ficar","querer","achar","enquanto","embora","cerca","alguma","atras","apesar","deixar","pra","mesmos","dessas","dada","breve","nelas","cheio","contra","afirmou","passou","los","grande","ver","horas","vamos","hehehe","humm","blabla","bla","blog","secs","haha","acontece","hmm","acho","minuto","minutos","previo","enfim","devidamente","assistir"] )




# Remove sinais de pontuaçao STRING --> STRING
def filter_punct (ent):
	punct = re.compile(r'[^\w\s@#]')  #Tags precisam ser mantidas, bem como @ 
	ent = punct.sub(' ', ent)
	
	return ent

# Remover caracteres repetidos em excesso, com o "o" em gooooooooooooooooool STRING --> STRING
def filter_charRepetition (ent):
	expRepeticao1 = re.compile('^([rs])\\1')
	expRepeticao2 = re.compile('([rs])\\1$')
	expRepeticao3 = re.compile('([^rs])\\1{1,}')
	expRepeticao4 = re.compile('([\\S\\s])\\1{2,}')
	
	ent = expRepeticao4.sub('\\1\\1', ent)
	ent = expRepeticao3.sub('\\1', ent)
	ent = expRepeticao2.sub('\\1', ent)
	ent = expRepeticao1.sub('\\1', ent)
	
	return ent
	
# Remove URL STRING --> STRING
def filter_url (ent):
	urlRef = re.compile("((https?|ftp):[\w\d:#@%/;\$()~_?\+-=\\\.&]*)")
	
	ent = urlRef.sub('', ent)
	return ent

# Retorna um SET contendo as N-gramas do texto STRING --> SET
def gen_NGrams(N,text, ignore_stops = True):
	NList = [] # start with an empty list
	if N > 1:
		partes = text.split() + (N *[''])
	else:
		partes = text.split()
	# append the slices [i:i+N] to NList
	for i in range(len(partes) - (N - 1) ):
		NList.append(partes[i:i+N])

	result = set()
	for item in NList:
		for i in xrange(1, N + 1):
			stops_found = [x for x in item[0:i] if x in stopwords or x == ""]
			#Ignora N-gramas so com stop words
			dado = ''.join(item[0:i])
			if (''.join(stops_found) != dado and dado != '') or ignore_stops == False:
				result.add(dado)
	return result
	
# Filtra Acentos String --> String
def filter_accents(s):
   return ''.join((c for c in unicode(unicodedata.normalize('NFKD', s).encode('ascii','ignore')) if unicodedata.category(c) != 'Mn'))
 
#Filtra Stopwords Set --> Set
def filter_stopwords(gramsSet):
	return gramsSet - stopwords
 
#Filtra numeros sozinhos Set --> Set
def filter_numbers(gramsSet):
	return [item for item in gramsSet if not item.isdigit()]
	
#Filtra termos menores que min_size  set--> Set
def filter_small_words(gramsSet, min_size):
	return [item for item in gramsSet if len(item)>= min_size]
#if __name__ == '__main__':
#	print type(stopswords)
