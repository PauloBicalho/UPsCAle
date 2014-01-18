# -*- coding: utf-8 -*-

import sys
import os
import getopt

from IO import *
from IO2 import getargs
from ProcessamentoTexto import *
from RotinasMatriz import gerar_matriz
from Caracterizacao import *
from Gera_matriz_transicao import *
from Clusterizacao import *
from Describe_topics import *

MAX_EIGENV = 1000
PRECISION = 0.01

def main():

	( arquivo_entrada, saida, tfIdf, preprocessar, ajustar, tecnica, AGRUPAR, representatividade, damp_factor, alpha, LANGUAGE, num_dimen ) = getargs()

	pasta_saida = gerar_diretorios_base( tecnica, saida)

	arquivo_atual = arquivo_entrada
	
	if preprocessar == True:
		print "\tRemovendo acentuação, pontuação, urls, etc... "
		arquivo_atual = preprocessar_texto(arquivo_entrada, pasta_saida + '/temp/preprocessado')
		print "\tFeito!"

	print "Removendo textos duplicados... "
	arquivo_atual = remover_duplicatas( arquivo_atual, pasta_saida + '/temp/uniq' )
	print "Feito!"

	if AGRUPAR == True:
		nome_saida = '.'.join( arquivo_atual.split('/')[-1].split('.')[:-1] ) + '_agrupado'
		arquivo_atual = agrupar_texto( arquivo_atual, pasta_saida + '/temp/' + nome_saida )
		arquivo_entrada = arquivo_atual

	
	print "Gerando o histograma... "
	arquivo_histograma = criar_histograma( arquivo_atual, pasta_saida + '/temp/histograma' )
	arquivo_palavras = arquivo_histograma
	print "Feito!"

	if preprocessar == True:
		print "Removendo stopwords... "
		arquivo_palavras = remover_stopwords(arquivo_histograma, pasta_saida + '/temp/palavras_validas', LANGUAGE)
		print "Feito!"

	arquivo_matriz = gerar_matriz(tecnica, arquivo_atual, arquivo_palavras, ajustar, tfIdf, pasta_saida + '/temp/matriz')

#	num_dimen = calc_representatividade( representatividade, arquivo_matriz, pasta_saida, MAX_EIGENV )
	print "\nnumero de dimensoes necessarias: %s\n" % num_dimen

	( arquivo_topPalavras ) = roda_tecnica( num_dimen, arquivo_matriz, tecnica, pasta_saida + '/firstOrderTopics/', PRECISION )

	(documentos_grupos, relevancia_grupos) = caracterizacao( pasta_saida + '/firstOrderTopics/', arquivo_matriz, arquivo_entrada, arquivo_topPalavras )

	gera_matriz_transicao( pasta_saida + '/firstOrderTopics/', num_dimen)

	(resultado_cluster) = clusterizacao_hierarquica( damp_factor, alpha, pasta_saida, num_dimen)
	
	describe_topics( pasta_saida )

	return

if __name__ == '__main__':
	main()

