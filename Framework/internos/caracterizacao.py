import sys
import operator
import time

if len(sys.argv) < 9:
	print "\nParametros: arquivo_basis.txt   arquivo_matriz_usuarios   arquivo_entrada_framework   valor   saida_tweets_grupos  saida_fernando   top25_palavras   saida_grupos_e_tweets\n\n"
	sys.exit()


#arquivo matriz_usuarios da pasta temp. Este arquivo mapeia diz qual documento uma dada coluna representa
arquivo_mapa = open( sys.argv[2], 'r' )

#no dicionario as chaves sao identificadores das colunas da matriz de entrada e cada valor representa o identificador do tweet no arquivo de entrada
print "1\n"
mapa_colunas = {}
for line in arquivo_mapa:
	line = line.split()
	mapa_colunas[ int(line[1]) ] = int( line[3] )

arquivo_mapa.close()


#set com todos os ids de documentos
print "2\n"
set_values = set( mapa_colunas.values() )
#for val in mapa_colunas.values():
#	set_values.add( int(val) )



print "3\n"
#arquivo de entrada ( do framework ) usado
arquivo_tweets = open( sys.argv[3], 'r' )

users = set()
tweets = {}
tweets_usuarios = {}
for line in arquivo_tweets:
	line = line.split('\t')
	usuario = int(line[0])
	identificador = int( line[1] )
	tweet = line[2].strip()

	if identificador in set_values:	
		tweets[ identificador ] = tweet

	if usuario not in users:
		users.add(usuario)

	if tweet not in tweets_usuarios:
		tweets_usuarios[tweet] = []

	tweets_usuarios[tweet].append(usuario)

arquivo_tweets.close()

print "4\n"
#arquivo basis.txt da saida do NNMF
entrada = open( sys.argv[1], 'r' )

saida_tweets_grupos = open( sys.argv[5] , 'w' )

grupos_tweets = {}
contador = -1
start_time = time.time()
for line in entrada:
 #       elapsed = time.time() - start_time
  #      print "\ta = %s\n" % elapsed
   #     start_time = time.time()

	contador += 1
	line = line.split()

	valores =  {}

	for i in range( len(line) ):
		valores[i] = float(line[i])
        
#        elapsed = time.time() - start_time
#        print "\tb = %s\n" % elapsed
#        start_time = time.time()

	sorted_valores = sorted(valores.iteritems(), key=operator.itemgetter(1), reverse = True)

#        elapsed = time.time() - start_time
#        print "\tc = %s\n" % elapsed
#        start_time = time.time()
	
        tweet_real = int( mapa_colunas[contador] )
	t = tweets[ tweet_real ].strip()
	print >> saida_tweets_grupos, "%i\t%s\t" % (tweet_real, t),
        
#        elapsed = time.time() - start_time
#        print "\td = %s\n" % elapsed
#        start_time = time.time()

	maior_valor = 0
	for i in range(int(sys.argv[4])):
                grupo_aux = int(sorted_valores[i][0])
                valor_aux = float(sorted_valores[i][1])
                conteudo = "%i\t%s" % ( tweet_real, t)
		if i == 0:
			print >> saida_tweets_grupos, "%s=%s " % (grupo_aux, valor_aux),
			maior_valor = valor_aux

			if grupo_aux not in grupos_tweets:
				grupos_tweets[ grupo_aux ] = set()
				grupos_tweets[ grupo_aux ].add( conteudo )
                        else:
			        if conteudo not in grupos_tweets[ grupo_aux ]:
				        grupos_tweets[ grupo_aux ].add( conteudo )

		else:
			if ( maior_valor - valor_aux ) < valor_aux:
				print >> saida_tweets_grupos, "%s=%s " % (grupo_aux, valor_aux),
			
				if grupo_aux not in grupos_tweets:
					grupos_tweets[ grupo_aux ] = set()
					grupos_tweets[ grupo_aux ].add( conteudo )
                                else:
				        if conteudo not in grupos_tweets[ grupo_aux ]:
					        grupos_tweets[ grupo_aux ].add( conteudo )
                        else:
                                break
			

	print >> saida_tweets_grupos, ""
        elapsed = time.time() - start_time  
        if( contador % 10000 ) == 0:
                print "\t%s" % contador
                print "\te = %s\n" % elapsed
                start_time = time.time()

entrada.close()
saida_tweets_grupos.close()




print "5\n"
grupos_usuarios	 = {}

contador = 0
total = 0
#para cada grupo, carrega os tweets associados e seus respectivos usuarios
for grupo in grupos_tweets:
	grupo = int(grupo)
	
	if grupo not in grupos_usuarios:
		grupos_usuarios[ grupo ] = set()

	for entry in grupos_tweets[ grupo ]:	
		entry = entry.split('\t')
		tweet = entry[1].strip()
		total += 1
		if tweet not in tweets_usuarios:
			contador += 1
			continue

		for u in tweets_usuarios[ tweet ]:
				grupos_usuarios[ grupo ].add( u )



print "6\n"
arquivo_top = open( sys.argv[7], 'r' )
cont = -1

vetores = {}
vetoresValor = {}
for line in arquivo_top:
	line = line.strip()

	if line.startswith('----------'):
		cont += 1
		vetores[ cont ] = []
		vetoresValor[ cont ] = []

	line = line.split('\t')
	if len( line ) >= 3 :
		vetores[ cont ].append( line[0]  )
		vetoresValor[ cont ].append( line[2] )
		

	
print "7\n"
saida_fernando = open( sys.argv[6], 'w' )
saida_grupos_e_tweets = open(sys.argv[8], 'w')

for grupo in grupos_tweets:
	print >> saida_fernando, "%s\t%s\t%s\t%s\t%s" % (grupo, float(len(grupos_tweets[grupo])) / float(len(tweets)), float(len(grupos_usuarios[grupo])) / float(len(users)), ",".join(vetores[ grupo ]), ",".join(vetoresValor[ grupo ]) )
		
	for tweet in grupos_tweets[ grupo ]:
		print >> saida_grupos_e_tweets, "%s\t%s" % (grupo, tweet.strip())


print "8\n"
print len(users)
print >> sys.stderr, "Erros: %s Em %s" % (contador,total)

