#!/bin/bash

INPUT_DB_NAME=$1;
LANGUAGE=$2;


for representativity in 0.35 0.4 0.45 0.5 0.55; do
     for dampFactor in 0.8 0.85 0.9 0.95 1.0; do

          python framework.py -i /largefiles2/tocunha/Inputs/${INPUT_DB_NAME}.txt -o /import/phocus6/tocunha/Outputs/${INPUT_DB_NAME}_TFIDF_R-${representativity}_D-${dampFactor} -m -p -a n -t NNMF -r ${representativity} -f ${dampFactor} -l ${LANGUAGE} -b 0.5 >>  /import/phocus6/tocunha/Outputs/Logs/log-${INPUT_DB_NAME}_TFIDF_R-${representativity}_D-${dampFactor}.txt

          rm -rf /import/phocus6/tocunha/Outputs/${INPUT_DB_NAME}_TFIDF_R-${representativity}_D-${dampFactor}/NNMF/temp

		  #python framework.py -i /largefiles2/tocunha/Inputs/${INPUT_DB_NAME}.txt -o /import/phocus6/tocunha/Outputs/${INPUT_DB_NAME}_TF_R-${representativity}_D-${dampFactor} -p -a n -t NNMF -r ${representativity} -f ${dampFactor} -l ${LANGUAGE} -b 0.5 >> /import/phocus6/tocunha/Outputs/Logs/log-${INPUT_DB_NAME}_TF_R-${representativity}_D-${dampFactor}.txt

		  #rm -rf /import/phocus6/tocunha/Outputs/${INPUT_DB_NAME}_TF_R-${representativity}_D-${dampFactor}/NNMF/temp

    done
done

