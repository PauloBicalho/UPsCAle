#!/bin/bash

INPUT_DB_NAME=$1;
LANGUAGE=$2;

for representativity in 0.35; do
  mkdir /import/phocus9/paulo/outputsFrameworkTesteFernando/${representativity};

  for amostra in 0 1 2; do

    mkdir /import/phocus9/paulo/outputsFrameworkTesteFernando/${representativity}/${amostra};

    python framework.py -i /scratch1/p.bicalho/databases/observatorioDB.txt -o /import/phocus9/paulo/outputsFrameworkTesteFernando/${representativity}/${amostra}/observatorioDB_TF_R-${representativity}_D-1/ -p -a n -t NNMF -r ${representativity} -f 1 -l portuguese -b 0.5  >> /import/phocus9/paulo/outputsFrameworkTesteFernando/${representativity}/${amostra}/Log-observatorioDB_TF_R-${representativity}_D-1.txt;
  
  done;
done;

