import sys
import os

from RotinasMatriz import gerar_matriz
from ProcessamentoTexto import *

NUM_DIMENSIONS = 100

def get_cut_point(precision, input_file):

	entrada = open(input_file, 'r')

	sigma = []
	contador = -1;
	for line in entrada:
		line = line.split()

		if contador > -1:
			sigma.append( float(line[0]) )

		contador+= 1

	num_items = contador
	sigma_norm = {}
	second_derivative = {}

	if num_items < 2:
		return 1

	second_norm = sigma[1]
	for i in range(num_items):
		sigma_norm[i]  = sigma[i] / second_norm
		second_derivative[i] = 0


	#curve approximating the second derivative 
	for i in range(1, num_items-1):
		second_derivative[i] = sigma_norm[i-1] - 2*sigma_norm[i] + sigma_norm[i+1]

	#search rank
	rank = num_items - 1;
	while (rank > 1):
		rank = rank - 1
		if abs(second_derivative[rank]) >= precision:
			break

	return rank

def describe_topics( documentos_grupos, resultado_cluster, AJUSTAR, TFIDF, precision, path, LANGUAGE):

	pasta_saida = path + '/TopicsDescription'
	os.system("mkdir -p %s" % pasta_saida)

        entrada = open( resultado_cluster, 'r' )
        output_file_name = pasta_saida + '/temp/selectedDocuments.txt'
        top_documents = pasta_saida + '/topDocuments.txt'
        top_terms = pasta_saida + '/topTerms.txt'

	os.system('rm -f %s' % (output_file_name) )
	os.system('rm -f %s' % (top_documents) )
	os.system('rm -f %s' % (top_terms) )

        for node in entrada:
		os.system("mkdir -p %s" % pasta_saida + '/temp' )

                node = node.strip().split('\t')
                nodeId = int(node[1].strip())
                leaves = node[3].strip()

                eigenvectors = leaves.strip().split(',');
                for eigenvector in eigenvectors:
                    os.system( 'grep "^%i\t" %s  >> %s ' % ( int(eigenvector) - 1, documentos_grupos, output_file_name ) )

		os.system( 'sort -u -nk 2 %s -o %s ' % ( output_file_name, output_file_name ) )

		arquivo_atual = preprocessar_texto( output_file_name, pasta_saida + '/temp/preprocessado')

		arquivo_atual = remover_duplicatas( arquivo_atual, pasta_saida + '/temp/uniq' )

                arquivo_histograma = criar_histograma( arquivo_atual, pasta_saida + '/temp/histograma' )

		arquivo_palavras = remover_stopwords(arquivo_histograma, pasta_saida + '/temp/palavras_validas', LANGUAGE)

                arquivo_matriz = gerar_matriz('SVD', arquivo_atual, arquivo_palavras, AJUSTAR, TFIDF, pasta_saida + '/temp/matriz')

		sufix = "/temp/topic_%s" % (nodeId)
		command = "internos/SVD/SVDLIBC/svd -d %s -r st -o %s %s" % (NUM_DIMENSIONS, pasta_saida + sufix , arquivo_matriz)
		os.system(command)

		arquivo_colunas = pasta_saida + '/temp/basis.txt'
		command = "tail -n +2 %s > %s" % ( pasta_saida + sufix + '-Vt', arquivo_colunas )
		os.system(command)

		arquivo_linhas = pasta_saida + '/temp/coordinates.txt'
		command = "tail -n +2 %s > %s" % ( pasta_saida + sufix + '-Ut', arquivo_linhas )
		os.system(command)
		description_size =  get_cut_point(precision,  pasta_saida + sufix + '-S' )

		selected_documents = pasta_saida + '/temp/topk_docs'
                os.system( 'cd internos/; matlab -r \"identify_topk_items(\'../%s\', \'../%s\', %i, %i ); quit\"; cd .. ' % ( arquivo_colunas, selected_documents, description_size, nodeId) )
		selected_terms = pasta_saida + '/temp/topk_terms'
                os.system( 'cd internos/; matlab -r \"identify_topk_items(\'../%s\', \'../%s\', %i, %i ); quit\"; cd .. ' % ( arquivo_linhas, selected_terms, description_size, nodeId) )

		os.system( 'perl internos/getOriginalItems.pl %s %s %s' % (selected_documents, pasta_saida + '/temp/matriz_colunas', top_documents) )
		os.system( 'perl internos/getOriginalItems.pl %s %s %s' % (selected_terms, pasta_saida + '/temp/matriz_linhas', top_terms) )

                os.system('rm -rf %s' % (pasta_saida + '/temp') )

        entrada.close()
 

        return

