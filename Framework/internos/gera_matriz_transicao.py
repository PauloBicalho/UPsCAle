import sys
import numpy as np

def usage():
        print '''Parametros:
        \t1 - Arquivo Coordinates
        \t2 - Arquivo Basis
        \t3 - Diretorio de saida
        \t4 - Prefixo do arquivo de saida
        '''

def parametros():

        if len(sys.argv) != 5:
                print '''Erro nos Parametros'''
                usage()
                sys.exit()


        nomeArq_coordinates = sys.argv[1]       #topicosXpalavras
        nomeArq_basis = sys.argv[2]             #tweetsXtopicos

        outDir = sys.argv[3]

        if not outDir.endswith('/'):
                outDir += '/'

        prefixo = sys.argv[4]

	modo = 2
	modo_valor = 0.5

        return (nomeArq_coordinates,nomeArq_basis,modo,modo_valor,outDir,prefixo)

def le_arquivo_vetores(arquivo):

        arquivo = open(arquivo,'r')

        vetores = []

        t = 0.000001

        linha = 0
        for line in arquivo:
                line = line.strip().split()
                valores = []

                for valor in line:
                        if float(valor) > t:
                                valores.append( float(valor) )
                        else:
                                valores.append( 0.0 )

                vetores.append(valores)

        num_colunas = len(line)

        arquivo.close()
        return np.matrix(vetores)

def normaliza_matriz( matriz ):

	m = np.matrix( matriz )

	for i in range(len(m)):
		if m[i].sum() == 0.0:
			continue
		m[i] /= m[i].sum()

	return m

def gera_matriz(vet_coordinates, vet_basis,outDir,prefixo,modo):


	#as matrizes de entrada original sao de documentos por topicos
	
	print "Normalizando Coordinates %s" % str(vet_coordinates.shape)
	coord = normaliza_matriz( vet_coordinates )  #documento X topico     normalizada por documento
	coordT = normaliza_matriz( vet_coordinates.transpose() )  #topico X documento      normalizada por topico

	print "Normalizando Basis %s" % str(vet_basis.shape)
	basis = normaliza_matriz( vet_basis )
	basisT = normaliza_matriz( vet_basis.transpose() )

	print "Gerando subMatriz C"
	subMatrizC = coordT * coord
	print "Feito %s" % str( subMatrizC.shape )

	print "Gerando subMatriz B"
	subMatrizB = basisT * basis
	print "Feito %s" % str( subMatrizB.shape )

	matrizFinal = ( subMatrizC + subMatrizB ) / 2.0

        return matrizFinal

def imprime_matriz(matriz,outDir,prefixo):

        arquivo = open(outDir + prefixo ,'w')

        (linhas,colunas) = matriz.shape

        for linha in range(linhas):
                for col in range(colunas):
                        print >> arquivo, "%s\t%s\t%s" % ( linha + 1, col + 1 , matriz[linha , col] )

        arquivo.close()


def main():

        (nomeArq_coordinates,nomeArq_basis,modo,modo_valor,outDir,prefixo) = parametros()

        print "Lendo arquivos de entrada..."

        vet_coordinates = le_arquivo_vetores(nomeArq_coordinates)
        vet_coordinates = vet_coordinates.transpose()   #fazendo a matriz virar termos por topicos

        vet_basis = le_arquivo_vetores(nomeArq_basis)

        print "Gerando a Matriz inicial..."
        matriz = gera_matriz(vet_coordinates,vet_basis,outDir,prefixo + "_matriz",modo)

        imprime_matriz(matriz,outDir,prefixo)

if __name__ == '__main__':
	main()
