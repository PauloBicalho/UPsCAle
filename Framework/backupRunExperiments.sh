#!/bin/bash

INPUT_DB_NAME=$1;
LANGUAGE=$2;

for representativity in 0.35 0.45 0.55; do
  mkdir /import/phocus9/paulo/outputsFrameworkHydra5/${representativity};

  for amostra in 0 1 2 3 4 5 6 7 8 9; do

    mkdir /import/phocus9/paulo/outputsFrameworkHydra5/${representativity}/amostra-${amostra};

    python framework.py -i /scratch1/p.bicalho/amostrasDatabases/observatorioDBAmostra_0.7-${amostra}.txt -o /import/phocus9/paulo/outputsFrameworkHydra5/${representativity}/amostra-${amostra}/observatorioDB_TF_R-${representativity}_D-1/ -p -a n -t NNMF -r ${representativity} -f 1 -l portuguese -b 0.5  >> /import/phocus9/paulo/outputsFrameworkHydra5/${representativity}/amostra-${amostra}/Log-observatorioDB_TF_R-${representativity}_D-1.txt;
  
  done;
done;

