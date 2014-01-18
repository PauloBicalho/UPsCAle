import os

def gera_matriz_transicao( pasta_entrada, num_dimen):

	command = "python internos/gera_matriz_transicao.py %s/coordinates.txt %s/basis.txt %s/ transitionMatrix_Dimen%s" % ( pasta_entrada, pasta_entrada, pasta_entrada, num_dimen )

	os.system( command )

	return
