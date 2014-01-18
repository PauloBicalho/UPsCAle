import sys
import os

from RotinasMatriz import gerar_matriz
from ProcessamentoTexto import *

DESCRIPTION_LENGTH = 30;

def describe_topics( path ):

	pasta_saida = path + '/TopicsDescription'
	os.system("mkdir -p %s" % pasta_saida)

	os.system("cut -f 2,7,8 %s > %s" % (path + '/SemanticClustering/clusterHierarchy.txt', pasta_saida + '/topTerms.txt') );
	os.system("perl internos/retrieveRelevantDocPerTopic.pl %s %s %s %s %g" % (path + '/firstOrderTopics/tweets_grupos', path + '/SemanticClustering/clusterHierarchy.txt', path + '/firstOrderTopics/relevancia_grupos', pasta_saida + '/topDocuments.txt', DESCRIPTION_LENGTH) );

        return

