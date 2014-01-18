import os

def clusterizacao_hierarquica( damp_factor, alpha, mode, pasta_entrada, pasta_saida, num_dimen):

	command = "mkdir -p %s/SemanticClustering;" % (pasta_entrada)
	os.system( command )

	print "Concatenando topicos latentes primarios... "
	command = "cd internos/SemanticClustering/; matlab -r \"mergeTopics(%f, %f, %i, \'%s/transitionMatrix_Dimen%s\', \'%s/SemanticClustering/\'); quit;\"; cd ../../;" % ( damp_factor, alpha, mode, pasta_entrada, num_dimen, pasta_saida)
#	command = "cd internos/SemanticClusteringOld/; matlab -r \"mergeTopics(%f, \'%s/firstOrderTopics/transitionMatrix_Dimen%s\', \'%s/SemanticClustering/\'); quit;\"; cd ../../;" % ( damp_factor, pasta_entrada, num_dimen, pasta_entrada)
	os.system( command )

	command = "perl internos/SemanticClustering/executeTopicMapping.pl %s/relevancia_grupos %s/SemanticClustering/clusteringMergedTopics.txt %s/SemanticClustering/clusterHierarchy.txt %s;" % (pasta_entrada, pasta_saida, pasta_saida, num_dimen)
#	command = "perl internos/SemanticClusteringOld/executeTopicMapping.pl %s/firstOrderTopics/relevancia_grupos %s/SemanticClustering/clusteringMergedTopics.txt %s/SemanticClustering/clusterHierarchy.txt %s;" % (pasta_entrada, pasta_entrada, pasta_entrada, num_dimen)
	os.system( command )

	return pasta_entrada + '/SemanticClustering/clusterHierarchy.txt'
