# -*- coding: utf-8 -*-

import sys

'''
Este programa recebe como entrada uma saida -Ut do SVD, a lista de termos e um inteiro X.
Para cada auto-vetor(linha) do arquivo de entrada é impresso na saida padrão os X maiores valores absolutos e seus respectivos termos.
'''

def busca_termos(arquivo):
	termos = {}
	for line in arquivo:
		if len(line.split()) == 0:
			break

		pos = int(line.split()[1])
		word = line.split()[3]
		
		termos[pos] = word

	return termos

def get_cut_point(num_items, precision, sigma):

	sigma_norm = {}
	second_derivative = {}

	second_norm = sigma[1][0]
	if second_norm == 0:
		return 1

	for i in range(num_items):
		sigma_norm[i]  = sigma[i][0] / second_norm
		second_derivative[i] = 0


	#curve approximating the second derivative 
	for i in range(1, num_items-1):
		second_derivative[i] = sigma_norm[i-1] - 2*sigma_norm[i] + sigma_norm[i+1]

	#search rank
	rank = num_items - 1;
	while (rank > 1):
		rank = rank - 1
		if abs(second_derivative[rank]) >= precision:
			break

	return rank

def main():
	entrada = open(sys.argv[1],'r')
	entrada2 = open(sys.argv[2],'r')
	precision = float(sys.argv[3])

	termos = busca_termos(entrada2)

	v = 0
	for line in entrada:
		line = line.split()

		list_valores = []

		contador = 0
		for valor in line:
			valor = (abs(float(valor)),contador)
			list_valores.append(valor)
			contador+= 1

		list_valores = sorted( list_valores, reverse=True )

		num_itens = get_cut_point(len(list_valores), precision, list_valores)
		print '\n ----------------------------------------------------------------------------'
		for i in range(num_itens):
			print '%s\t=\t%s' % ( termos[list_valores[i][1]],line[list_valores[i][1]] )

		v += 1
		if ( v % 25 ) == 0:
			print >> sys.stderr, 'Ja foram processadas %s linhas' % v
		
if __name__ == '__main__':
	main()
