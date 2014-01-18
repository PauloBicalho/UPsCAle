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
	print "\t-d Modo de execucao do algoritmo de agrupamento (1- Min; 2-Mean; 3- Max)"
	print "\t-f Damp Factor (0.0 to 1.0)"
	print "\t-l Language"
	print "\t-b cohesion relevance (from 0 to 1)"
        print "\t-z caso ja tenha a matriz gerada passar neste parametro"
        print "\t-x caso ja saiba o numero de dimensoes"
        print "\t-d e valor 1, 2 ou 3 para utilizar min avg e max"
        print "\t-w caso ja tenha computado o NNMF passar neste parametro"
	print "\n"

def getargs():
	try:
          opts, args = getopt.getopt(sys.argv[1:], "i:mpa:t:o:g:r:d:f:l:b:z:x:d:w:")
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
        mode = 1
	LANGUAGE = None
	
        MATRIZ = None
        DIMEN_NUM = None
        SAIDA_NNMF = None
	for opt,arg in opts:
		if opt == "-i":
			arquivo_entrada = arg
                elif opt == "-z":
                        MATRIZ = arg
                elif opt == "-x":
                        DIMEN_NUM = int(arg)
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
		elif opt == "-d":
			mode = int( arg.strip() )
		elif opt == "-b":
			alpha = float( arg.strip() )
		elif opt == "-g":
			AGRUPAR = True
		elif opt == "-l":
			LANGUAGE = arg
		elif opt == "-w":
			SAIDA_NNMF = arg

		else:
			assert False, "Opcao Desconhecida"

	if( arquivo_entrada == None or pasta_saida == None or tecnica == None or LANGUAGE == None or rep == None ):

		print "Faltam argumentos"
		usage()
		sys.exit(2)


	return( arquivo_entrada, pasta_saida, tfIdf, preprocessar, ajustar, tecnica, AGRUPAR, rep, damp_factor, alpha, mode, LANGUAGE, MATRIZ, DIMEN_NUM, SAIDA_NNMF )


def gerar_diretorios_base( tecnica, saida):

	comando = "mkdir -p %s/%s" % (saida, tecnica)
	os.system( comando )
	os.system( comando + "/temp" )
	os.system( comando + "/firstOrderTopics" )
	os.system( comando + "/SemanticClustering" )
	os.system( comando + "/TopicsDescription" )

	pasta_saida = "%s/%s/" % (saida, tecnica)

	return pasta_saida

