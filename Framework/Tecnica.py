# -*- coding: utf-8 -*-
import sys
import os

MAX_ITER = 10
MAX_SIZE = 10000
SPARSITY_LEVEL = 0.15

sys.path.append('internos/')

def calc_representatividade( valor_ref, matriz, saida, MAX_EIGENV ):

	path = saida + '/temp/svd/'
	os.system( 'mkdir -p ' + path )
	print "\n-----==============================================================================================================-----"
	print "Calculando o número de vetores necessários para atingir %s%% de representatividade" % (valor_ref * 100)

	command = "perl internos/change_matrix_format.pl %s %s_redsvd" % (matriz, matriz)
	os.system(command)

	command = "redsvd -i %s_redsvd -o %s/SVDOutput -r %i -f sparse -m SVD" % (matriz, path, MAX_EIGENV)
	os.system(command)

	command = "cd internos; matlab -r \"getNumEigenVectors(\'%s\', %i, %g, \'%s\' ); quit\"; cd ..;" % ( path + '/SVDOutput.S', MAX_SIZE, valor_ref, path + '/numEigenValues.txt')
	os.system(command)

	arquivo_S = open( path + '/numEigenValues.txt', 'r' )
        
	for line in arquivo_S:
		num_vetores_necessarios = int( line.strip() )
        arquivo_S.close()
        
        command = "rm -rf %s" % path
        os.system(command)

	return num_vetores_necessarios


def roda_tecnica( dimen, matriz, modo, pasta_saida, precision):
	
	sufix = "/%s_%s" % (modo,dimen)

	if modo == 'NNMF':

		command = "perl internos/generateInputFormat.pl %s %s" % ( matriz, '/'.join( matriz.split('/')[0:-1] ) + '/triplets'  )
		os.system(command)

		os.system( 'cd internos; matlab -r \"multiplicativeMethod(\'%s\', 100, %s, \'%s\' ); quit\"; cd .. ' % ( '/'.join( matriz.split('/')[0:-1] ) + '/triplets', dimen, pasta_saida ) )
	#	os.system( 'cd internos; matlab -r \"multiplicativeMethod(\'%s\', 100, %s, \'%s\' ); quit\"; cd .. ' % ( '/'.join( matriz.split('/')[0:-1] ) + '/triplets', dimen, pasta_saida ) )
		#os.system( 'cd internos/NNMF/; matlab -r \"snmfsc(\'%s\', %i, %g, %g, 0, %i, \'%s\' ); quit\"; cd ../' % ( '/'.join( matriz.split('/')[0:-1] ) + '/triplets', dimen, SPARSITY_LEVEL, SPARSITY_LEVEL, MAX_ITER, pasta_saida ) )

		command = "cd ../../;"
		os.system(command)
		
	else: 

		command = "internos/SVD/SVDLIBC/svd -d %s -r st -o %s %s" % (dimen, pasta_saida + sufix , matriz)
		os.system(command)
		
		command = "tail -n +2 %s > %s" % ( pasta_saida + sufix + '-Vt', pasta_saida + '/tBasis.txt' )
		os.system(command)

		command = "perl internos/transposeLines.pl %s %s" % (pasta_saida + '/tBasis.txt', pasta_saida + '/basis.txt' )
		os.system(command)

		command = "tail -n +2 %s > %s" % ( pasta_saida + sufix + '-Ut', pasta_saida + '/coordinates.txt' )
		os.system(command)

		command = "rm -rf %s %s/SVD-*" % (pasta_saida + '/tBasis.txt', pasta_saida)
		os.system(command)

	command = "python internos/topX.py %s %s %f > %s" % (pasta_saida + '/coordinates.txt', matriz + "_linhas", precision, pasta_saida + "/topK_palavras" ) 
	os.system(command)
	print "Feito - Resultado em: %s" % ( "topK_" + matriz )


	#return ( pasta_saida + "/topK_palavras" )
        return 

