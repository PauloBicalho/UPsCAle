import os

def caracterizacao( pasta_entrada, arquivo_matriz, arquivo_texto):
        arquivo_top = pasta_entrada  + "/topK_palavras"

	command = "python internos/caracterizacao.py %s/basis.txt %s_colunas %s 3 %s/tweets_grupos %s/relevancia_grupos %s %s/grupos_e_tweets" % ( pasta_entrada, arquivo_matriz, arquivo_texto, pasta_entrada, pasta_entrada, arquivo_top, pasta_entrada )

	os.system( command )

	return ( pasta_entrada + '/grupos_e_tweets', pasta_entrada + '/relevancia_grupos'  )
