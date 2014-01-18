#!/bin/bash

INPUT_DB_NAME=$1;
LANGUAGE=$2;
NUM_TOPICS=$3 

for representativity in 0.35 0.4 0.45 0.5 0.55; do
     for dampFactor in 0.8 0.85 0.9 0.95 1.0; do

# python framework.py -i /largefiles2/tocunha/Inputs/${INPUT_DB_NAME}.txt -o /import/phocus6/tocunha/Outputs/${INPUT_DB_NAME}_TFIDF_R-${representativity}_D-${dampFactor} -m -p -a n -t NNMF -r ${representativity} -f ${dampFactor} -l ${LANGUAGE} -b 0.5 >>  /import/phocus6/tocunha/Outputs/Logs/log-${INPUT_DB_NAME}_TFIDF_R-${representativity}_D-${dampFactor}.txt

# rm -rf /import/phocus6/tocunha/Outputs/${INPUT_DB_NAME}_TFIDF_R-${representativity}_D-${dampFactor}/NNMF/temp

          python frameworkSVD.py -i /scratch1/tocunha/Inputs/${INPUT_DB_NAME}.txt -o /import/phocus9/tocunha/Outputs/TC/${INPUT_DB_NAME}_TF_R-${representativity}_D-${dampFactor} -p -a n -t NNMF -r ${representativity} -f ${dampFactor} -l ${LANGUAGE} -b 0.5 -n ${NUM_TOPICS} >> /import/phocus9/tocunha/Outputs/TC/log-${INPUT_DB_NAME}_TF_R-${representativity}_D-${dampFactor}.txt

          #exit;

          rm -rf /import/phocus9/tocunha/Outputs/TC/${INPUT_DB_NAME}_TF_R-${representativity}_D-${dampFactor}/NNMF/temp

         # reset 

    done
done

