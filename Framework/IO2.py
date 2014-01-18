# -*- coding: utf-8 -*-
import os
import getopt
import sys

def usage():
	print "ARGS:\n"
	print "\t-i Nome :Arquivo de entrada com os dados"
	print "\t-o Nome :Prefixo de saida."
	print "\t-m :Utilizar TF x IDF ao invés de somente TF nas células da matriz "
	print "\t-p: Realiza pré-processamento nos dados (ignora palavras em Maiúsulas) inclui: "
	print "\t\tRemove stop-words "
	print "\t\tRemove conjugações verbais"
	print "\t\tRemove plural e converte feminimo para masculino"
	print "\t-a [ s | n ] : Habilita ou desabilita o ajuste de valores (padrao habilitado), inclui:"
	print "\t\tNormalização da frequência"
	print "\t\tMedia zero em linhas e colunas"
	print "\t-t [ SVD | PCA | NNMF ]  : Técnica utilizada"
	print "\t-r Valor : Valor base para o calculo do numero de dimensões"
	print "\t-g Agrupar por usuário"
	print "\t-f Damp Factor (0.0 to 1.0)"
	print "\t-l Language"
	print "\t-b cohesion relevance (from 0 to 1)"
	print "\t-n numero de topicos da base"
	print "\n"

def getargs():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "i:mpa:t:o:g:r:d:f:l:b:n:")
	except:
		#print str(err)
		usage()
		sys.exit(2)

	arquivo_entrada = None
	pasta_saida = None
	tecnica = None

	tfIdf = False
	preprocessar = False
	ajustar = False
	AGRUPAR = False
	damp_factor = 0.95
	alpha = 0.5
	LANGUAGE = None
	num_dimen = 6

	for opt,arg in opts:
		if opt == "-i":
			arquivo_entrada = arg
		elif opt == "-t":
			tecnica = arg
		elif opt == "-p":
			preprocessar = True
			
		elif opt == "-a":
			if arg == 'n' or arg == 'N':
				ajustar = False
			elif arg == 's' or arg == 'S':
				ajustar = True
			else:
				print "Parametro -a invalido"
				sys.exit(2)

		elif opt == "-m":
			tfIdf = True	

		elif opt == "-r":
			rep = float( arg.strip() )

		elif opt == "-o":
			pasta_saida = arg
		elif opt == "-f":
			damp_factor = float( arg.strip() )
		elif opt == "-b":
			alpha = float( arg.strip() )
		elif opt == "-g":
			AGRUPAR = True
		elif opt == "-l":
			LANGUAGE = arg
		elif opt =="-n":
			num_dimen = int( arg.strip() )
		else:
			assert False, "Opcao Desconhecida"

	if( arquivo_entrada == None or pasta_saida == None or tecnica == None or LANGUAGE == None or rep == None ):

		print "Falta argumentos"
		usage()
		sys.exit(2)


	return( arquivo_entrada, pasta_saida, tfIdf, preprocessar, ajustar, tecnica, AGRUPAR, rep, damp_factor, alpha, LANGUAGE, num_dimen )


def gerar_diretorios_base( tecnica, saida):

	comando = "mkdir -p %s/%s" % (saida, tecnica)
	os.system( comando )
	os.system( comando + "/temp" )
	os.system( comando + "/firstOrderTopics" )
	os.system( comando + "/SemanticClustering" )
	os.system( comando + "/TopicsDescription" )

	pasta_saida = "%s/%s/" % (saida, tecnica)

	return pasta_saida

