# -*- coding: utf-8 -*-

import sys
import os
import getopt

from IO import *
from ProcessamentoTexto import *
from RotinasMatriz import gerar_matriz
from Caracterizacao import *
from Gera_matriz_transicao import *
from Clusterizacao import *
from Describe_topics import *

MAX_EIGENV = 1000
PRECISION = 0.01

def main():

	( arquivo_entrada, saida, tfIdf, preprocessar, ajustar, tecnica, AGRUPAR, representatividade, damp_factor, alpha, mode, LANGUAGE, MATRIZ, DIMEN_NUM, SAIDA_NNMF ) = getargs()

	pasta_saida = gerar_diretorios_base( tecnica, saida)

        if SAIDA_NNMF == None:        
          if MATRIZ == None:
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

          else:
                  print "MATRIZ INFORMADA\n"
                  arquivo_matriz = MATRIZ

          if DIMEN_NUM == None:
            num_dimen = calc_representatividade( representatividade, arquivo_matriz, pasta_saida, MAX_EIGENV )
            DIMEN_NUM = num_dimen
          else:
            num_dimen = DIMEN_NUM
          

          #( arquivo_topPalavras ) = roda_tecnica( num_dimen, arquivo_matriz, tecnica, pasta_saida + '/firstOrderTopics/', PRECISION )
          roda_tecnica( num_dimen, arquivo_matriz, tecnica, pasta_saida + '/firstOrderTopics/', PRECISION )

   	  #(documentos_grupos, relevancia_grupos) = caracterizacao( pasta_saida + '/firstOrderTopics/', arquivo_matriz, arquivo_entrada, arquivo_topPalavras )
	  (documentos_grupos, relevancia_grupos) = caracterizacao( pasta_saida + '/firstOrderTopics/', arquivo_matriz, arquivo_entrada )

	  gera_matriz_transicao( pasta_saida + '/firstOrderTopics/', num_dimen)
          saida_nnmf = pasta_saida + '/firstOrderTopics/'
        
        else: 
          saida_nnmf = SAIDA_NNMF
          
        if DIMEN_NUM == None:
          num_dimen = calc_representatividade( representatividade, arquivo_matriz, pasta_saida, MAX_EIGENV )
        else:
          num_dimen = DIMEN_NUM
          
        print "\nnumero de dimensoes necessarias: %s\n" % num_dimen
	(resultado_cluster) = clusterizacao_hierarquica( damp_factor, alpha, mode, saida_nnmf, pasta_saida, num_dimen)
	describe_topics( pasta_saida )

	return

if __name__ == '__main__':
	main()

