#!/bin/bash

for v in {500,1000,2000}
do
	comand="./svd -d $v -r st -o ../output/matrizTF$v ../inputs/matriz_rel_tf_filtrada.txt"
	$comand

	comand2="python /scratch/paulo/topX.py SVD/outputs/matrizTF$v-Ut /python/hist_rel_filtrado.txt 
done


