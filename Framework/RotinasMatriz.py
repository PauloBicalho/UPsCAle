# -*- coding: utf-8 -*-
import os
import sys	

sys.path.append('internos/')

#from MatrizTf import gera_matrizTf
from Matriz import gera_matrizTf

def gerar_matriz(modo, arquivo_entrada, arquivo_palavras, AJUSTAR, TFIDF, arquivo_saida):

	PCA = False
	if modo == 'PCA':
		PCA = True
	
	LOG = False
	NORM = False
	MEDIA_LINHA = False
	MEDIA_COLUNA = False
	
	if AJUSTAR == True:
		if modo == 'SVD':
			LOG = True

		NORM = True
		
		if modo != 'NNMF':
			MEDIA_LINHA = True
			MEDIA_COLUNA = True

	if TFIDF == True:
		TFIDF = True
	
	gera_matrizTf( arquivo_entrada, arquivo_palavras, arquivo_saida, PCA, LOG, NORM, MEDIA_LINHA, MEDIA_COLUNA, TFIDF )	

	return arquivo_saida 


