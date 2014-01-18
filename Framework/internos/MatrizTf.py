import sys
import operator
from math import sqrt,log
from unicodedata import normalize

#normalize('NFKD', palavra).encode('ASCII','ignore')


#variavel global que conta o frequencia de cada palavra na matriz gerada. (se uma palavra nao aparecer nenhuma vez, deve ser eliminada para nao interferir no SVD
counter_words = {}
num_tweets = {}
users_por_word = {}

#variavel global que conta o numero de valores nao zero na matriz. Atualizado na funcao update_hist
nao_zero = 0

def get_words(file_words):
	words = {}
	contador = -1
	
	for line in file_words:
		contador += 1
		word = line.split('\t')[0].lower()
		word = normalize('NFKD',unicode(word) ).encode('ASCII','ignore')
		
		if word not in words:
			words[word] = contador
			counter_words[word] = 0
			users_por_word[word] = set()

	return words


def update_hist(user_id,tweet,words,hist):
	global nao_zero
	global users_por_word

	verify = 0
	for word in tweet.split():
		if word in words:
			verify = 1

			if word not in users_por_word:
				users_por_word[word] = set()

			if user_id not in users_por_word[word]:
				users_por_word[word].add(user_id)

			if word not in hist:
				hist[word] = 0
				nao_zero += 1 #variavel global

			hist[word] += 1
			counter_words[word] += 1

			if hist[word] >= 500:
				counter_words[word] -= hist[word]
				nao_zero -= 1
				hist.pop(word)
			

	return verify


def create_user_hist(file_tweets,words):
	global user_tweets
	global nao_zero
	global users_por_word
	global num_tweets

	users_hist = {}
	for line in file_tweets:
		line = line.split('\t')
		
		user_id = "%s" % (line[1])
		
		tweet = normalize('NFKD',unicode(line[2].lower()) ).encode('ASCII','ignore')
		
		if user_id not in users_hist:
			users_hist[user_id] = {}

		if user_id not in num_tweets:
			num_tweets[user_id] = 0

		num_tweets[user_id] += update_hist(user_id,tweet,words,users_hist[user_id])


	new = {}
	for user in users_hist:
		if len(users_hist[user]) > 3:
			new[user] = users_hist[user]

		else:
			for word in users_hist[user]:
				nao_zero -= 1
				counter_words[word] -= users_hist[user][word] 
				users_por_word[word].remove(user)
			
	del(users_hist)
	return new


def print_user(f,prefix,users_tweets):
	
	contador = 0
	for user_id in users_tweets:
		f.write( '%s %s =\t%s\n' % (prefix,contador,user_id) )
		contador += 1

	return

#imprime as palavras em um arquivo e a retira as palavras que nao aparacem na matriz
def update_and_print_words(f,prefix,words,users_hist):
	global users_por_word

	retirado = 0
	temp = dict(words)
	for word,val in sorted( temp.iteritems(), key=operator.itemgetter(1) ):
		words[word] -= retirado

		if len( users_por_word[word] ) == 0:
			print "rs"
			retirado += 1
			words.pop(word)

	sorted_words = sorted(words.iteritems(), key=operator.itemgetter(1))
	for word,pos in sorted_words:
		f.write( '%s %s = \t%s\n ' % (prefix,pos,word) )


	print "Retirado %s" % retirado
	return

def calc_media(hist):
	
	tot = 0
	for val in hist.itervalues():
		tot += val

	media = float(tot) / float(len(hist))

	return media

def gera_matrizTf( nome_file_tweets, nome_file_words, nome_saida, PCA, LOG, NORM, MEDIA_LINHA, MEDIA_COLUNA, TFIDF ):
	
	file_tweets = open(nome_file_tweets,'r')
	file_words = open(nome_file_words,'r')
	file_saida = open(nome_saida,'w')

	saida_words = open(nome_saida + '_palavras','w')
	saida_users = open(nome_saida + '_usuarios','w')
#	modo = sys.argv[4].split(',')


	print 'Obtendo Palavras\n'
	words = get_words(file_words)

	print 'Criando TF dos usuario\n'
	users_hist = create_user_hist(file_tweets,words)
	
	print 'Atualizando e imprindo as Palavras no arquivo: %s\n' % ('palavras_' + sys.argv[3])
	update_and_print_words(saida_words,'linha',words,users_hist)

	print 'Imprimindo os Usuarios no arquivo: %s\n' % ( 'usuarios_' + sys.argv[3] )
	print_user(saida_users,'coluna',users_hist)


	print 'Gerando a Matriz\n'

#	sys.stdout = file_saida

	lines = len(words)
	cols = len(users_hist)

	print >> file_saida, '%s %s %s' % ( lines, cols, nao_zero )

	global num_tweets
	i = 0
	for user_id in users_hist:
		hist = users_hist[user_id]
		print >> file_saida, len(hist)

		med_col = calc_media( hist )

		for word in hist:
			if NORM == True:
				hist[word] =  float( hist[word] ) /  float(num_tweets[int(user_id)])

			if TFIDF == True:
				hist[word] = float(hist[word]) * float( log( float(cols) / float( len(users_por_word[ word ]) )) )

			if PCA == True:
				media = calc_media(hist)
				denominador = sqrt( float( cols - 1.0 ) )
				t = hist[word]
				hist[word] = ( float( hist[word] ) - media ) / denominador

			if LOG == True and hist[word] != 0.0:
				hist[word] = log( hist[word] )

				
			if MEDIA_LINHA == True:
				media_linha = float( counter_words[ word ] ) / float( len(users_por_word[ word ]) )
 				hist[word] = float( hist[word] ) - media_linha
			
			elif MEDIA_COLUNA == True:
				#media = calc_media(hist)
				hist[word] = ( float( hist[word] ) - med_col )

			if not ( MEDIA_LINHA == True and MEDIA_COLUNA == True ):
				print >> file_saida, '%s %s' % ( words[word], hist[word] )


		if MEDIA_LINHA == True and MEDIA_COLUNA == True:
			med_col2 = calc_media( hist )
			for word in hist:
				hist[word] = ( float( hist[word] ) - med_col2 )
			
				print >> file_saida, '%s %s' % ( words[word], hist[word] )


		i += 1
		if i % 250 == 0:
			print "ja foram preenchidas %s colunas" % i
	
	
	file_tweets.close()
	file_words.close()
	file_saida.close()
	saida_words.close()
	saida_users.close()

	return
