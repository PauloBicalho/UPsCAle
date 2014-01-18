import sys
import operator

if len(sys.argv) < 9:
	print "\nParametros: arquivo_basis.txt   arquivo_matriz_usuarios   arquivo_entrada_framework   valor   saida_tweets_grupos  saida_fernando   top25_palavras   saida_grupos_e_tweets\n\n"
	sys.exit()


#aruqivo matriz_usuarios da pasta temp
arquivo_mapa = open( sys.argv[2], 'r' )

#no dicionario as chaves sao identificadores das colunas da matriz de entrada e cada valor representa o identificador do tweet no arquivo de entrada
mapa_colunas = {}
for line in arquivo_mapa:
	line = line.split()
	mapa_colunas[ int(line[1]) ] = int( line[3] )

arquivo_mapa.close()


set_values = set( mapa_colunas.values() )
#for val in mapa_colunas.values():
#	set_values.add( int(val) )



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

#arquivo basis.txt da saida do NNMF
entrada = open( sys.argv[1], 'r' )

saida_tweets_grupos = open( sys.argv[5] , 'w' )

grupos_tweets = {}
contador = -1
for line in entrada:
	contador += 1
	line = line.split()

	valores =  {}

	for i in range( len(line) ):
		valores[i] = float(line[i])

	sorted_valores = sorted(valores.iteritems(), key=operator.itemgetter(1), reverse = True)

	tweet_real = int( mapa_colunas[contador] )
	t = tweets[ tweet_real ].strip()
	print >> saida_tweets_grupos, "%i\t%s\t" % (tweet_real, t),

	maior_valor = 0
	for i in range(int(sys.argv[4])):
		if i == 0:
			print >> saida_tweets_grupos, "%s=%s " % (sorted_valores[i][0], sorted_valores[i][1]),
			maior_valor = float( sorted_valores[i][1] )

			if int(sorted_valores[i][0]) not in grupos_tweets:
				grupos_tweets[ int(sorted_valores[i][0]) ] = []

			
			if t not in grupos_tweets[ int(sorted_valores[i][0]) ]:
				grupos_tweets[ int(sorted_valores[i][0]) ].append( "%i\t%s" % (tweet_real, t ) )

		else:
			if ( maior_valor - float( sorted_valores[i][1] ) ) < float( sorted_valores[i][1] ):
				print >> saida_tweets_grupos, "%s=%s " % (sorted_valores[i][0], sorted_valores[i][1]),
			
				if int(sorted_valores[i][0]) not in grupos_tweets:
					grupos_tweets[ int(sorted_valores[i][0]) ] = []
				
				if t not in grupos_tweets[ int(sorted_valores[i][0]) ]:
					grupos_tweets[ int(sorted_valores[i][0]) ].append( "%i\t%s" % (tweet_real, t ) )
			

	print >> saida_tweets_grupos, ""

entrada.close()
saida_tweets_grupos.close()




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

			if u not in grupos_usuarios[ grupo ]:
				grupos_usuarios[ grupo ].add( u )



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
		

	
saida_fernando = open( sys.argv[6], 'w' )
saida_grupos_e_tweets = open(sys.argv[8], 'w')

for grupo in grupos_tweets:
	print >> saida_fernando, "%s\t%s\t%s\t%s\t%s" % (grupo, float(len(grupos_tweets[grupo])) / float(len(tweets)), float(len(grupos_usuarios[grupo])) / float(len(users)), ",".join(vetores[ grupo ]), ",".join(vetoresValor[ grupo ]) )
		
	for tweet in grupos_tweets[ grupo ]:
		print >> saida_grupos_e_tweets, "%s\t%s" % (grupo, tweet.strip())


print len(users)
print >> sys.stderr, "Erros: %s Em %s" % (contador,total)

