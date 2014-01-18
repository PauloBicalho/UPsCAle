import sys

def recupera_palavras_validas( arquivo_palavras ):
	entrada = open( arquivo_palavras, 'r' )
	
	palavras_validas_m1 = {}
	palavras_validas_m2 = {}
	
	contador = 0
	for line in entrada:
		line = line.strip().split('/t')
		palavra = line[0].lower()
		
		if palavra not in palavras_validas_m1:
			palavras_validas_m1[ palavra ] = contador   #cada palavra sera uma linha, o contador indica qual o indice
			palavras_validas_m2[ contador ] = palavra
			
			contador += 1
	
	entrada.close()
	
	return palavras_validas_m1,palavras_validas_m2

def inicializa_dicionario( chaves, valor ):
	d = {}
	
	for chave in chaves:
		d[chave] = valor

def gera_histograma_textos( arquivo_texto, mapa_palavra_id, mapa_id_palavra ):
	
	entrada = open( arquivo_texto, 'r')
	
	palavras_validas = set( mapa_palavra_id.keys() )
	nao_zero = 0
	
	#num_textos_por_palavra = inicializa_dicionario( mapa_id_palavra.keys(), 0 )  #valor e o id da palavra
	num_textos_por_palavra = inicializa_dicionario( mapa_palavra_id.keys(), [] )  #valor e o id da palavra
	frequencia_palavra = inicializa_dicionario( mapa_palavra_id.keys(), 0 )
	
	hist_textos = {}
	for line in entrada:
		line = line.strip().split('/t')
		
		u_id = line[0]
		t_id = line[1]
		
		texto = line[2]
		
		hist = {}
		for palavra in texto.split():
			if palavra in palavras_validas:
				#id_palavra = palavras_validas[ palavra ]
				#if id_palavra not in hist:
				#	hist[ id_palavra ] = 0
				#hist[ id_palavra ] += 1
				
				if palavra not in hist:
					hist[ palavra ] = 0
				
				hist[ palavra ] += 1
		
		if len( hist ) <= 3:
			continue
		
#		for id_palavra in hist:
		for palavra in hist:
#			palavra = mapa_id_palavra[ id_palavra ]
#			num_textos_por_palavra[ id_palavra ] += 1
			#frequencia_palavra[ palavra ] += hist[ id_palavra ]
			
			frequencia_palavra[ palavra ] += hist[ palavra ]
			num_textos_por_palavra[ palavra ].append( t_id )
			
		nao_zero += len( hist )
		hist_textos[ t_id ] = hist
	
	entrada.close()
	
	return hist_textos,nao_zero,frequencia_palavra,num_textos_por_palavra

def normaliza_histograma( hist ):
	
	soma = sum( hist.values() )
	
	for p_id in hist:
		hist[ p_id ] /= float(soma)
		
	return hist
	
def verifica_uso_palavras( frequencia_palavra, mapa_palavra_id, mapa_id_palavra ):
	
	retirada = 0
	log = open( "palavras_retiradas", 'w' )
	for palavra in frequencia_palavra:
		mapa_palavra_id[ palavra ] -= retirada
		novo_id = mapa_palavra_id[ palavra ]
		
		mapa_id_palavra[ novo_id ] = palavra
		
		
		if frequencia_palavra[ palavra ] == 0:
			print >> log, palavra
			id_invalido = mapa_palavra_id[ palavra ]
			
			mapa_palavra_id.pop( palavra )
			mapa_id_palavra.pop( id_invalido )
			
			retirada += 1
			
	log.close()
	return mapa_palavra_id,mapa_id_palavra

def imprime_palavra( mapa_id_palavra, arquivo_saida ):
	saida_palavras = open( arquivo_saida + '_linhas', 'w' )
	
	for palavra_id in sorted( mapa_id_palavra.keys):
		print >> saida_palavras, "Linha %s = %s" % (palavra_id, mapa_id_palavra[ palavra_id ])
	
	saida_palavras.close()
	
def imprime_texto( texto_ordenados ,arquivo_saida ):
	
	saida_textos = open( arquivo_saida + '_colunas', 'w' )
	
	contador = 0
	for t_id in textos_ordenados:
		print >> saida_textos, "Coluna %s = %s" % (contador, t_id)
		contador += 1
	
	saida_textos.close()

def gera_matrizTF( arquivo_texto, arquivo_palavras, arquivo_saida, PCA, LOG, NORM, MEDIAL, MEDIAC, TFIDF ):
	
	mapa_palavra_id,mapa_id_palavra = recupera_palavras_validas( arquivo_palavras )
	
	(histograma_textos,nao_zero,frequencia_palavra,num_textos_por_palavra) = gera_histograma_textos( arquivo_texto, mapa_palavra_id, mapa_id_palavra )
	
	mapa_palavra_id,mapa_id_palavra = verifica_uso_palavras( frequencia_palavra, mapa_palavra_id, mapa_id_palavra )
	
	
	linhas = len(mapa_palavra_id)
	colunas = len(histograma)
	
	imprime_palavras( mapa_id_palavra, arquivo_saida ):
	imprime_textos( sorted( histograma_textos.keys() ), arquivo_saida)
	
	
	saida = open( arquivo_saida, 'w')
	print >> saida "%s %s %s" % (linhas, colunas, nao_zero)
	
	denominador_pca = sqrt( float(colunas -1) )
	
	contador = 0
	for t_id in histograma_textos:
		hist = histograma_texto[ t_id ]
		media_coluna = sum( hist.values() ) / float( len(hist.values() )
		
		if NORM:
			hist = normaliza_histograma( hist )
		
		print >> saida, "%s" % ( len(hist) )
		for palavra in hist:
			
			if TFIDF:
				hist[ palavra ] = hist[ palavra ] * float( log( colunas / float( len(num_textos_por_palavra[palavra]) ) ) )
				
			if PCA:
				hist[ palavra ] = ( hist[palavra] - media_coluna ) / denominador_pca
				
			if LOG and hist[palavra_id] != 0:
				hist[palavra] = log( hist[palavra] )
				
			if MEDIAL:
				media_linha = frequencia_palavra[ palavra ] / float( num_textos_por_palavra[ palavra ] )
				hist[ palavra ] -= media_linha
				
			elif MEDIAC:
				hist[ palavra ] -= media_coluna
				
			if not MEDIAC and MEDIAL:
				print >> saida, "%s %s" % (mapa_palavra_id[ palavra ], hist[ palavra ] )
				
		if MEDIAC and MEDIAL:
			n_media = sum( hist.values() ) / float( len( hist.values() ) )
			for palavra in hist:
				hist[palavra] -= n_media
				print >> saida, "%s %s" % (mapa_palavra_id[ palavra ], hist[ palavra ] )
				
				
		if contador % 250 == 0:
			print "ja foram preenchidas %s colunas" % contador
		contador += 1
				
	saida.close()
	
