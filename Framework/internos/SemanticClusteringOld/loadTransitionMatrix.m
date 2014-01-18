function [irreducibleMatrix, numTopics] = loadTransitionMatrix(dampFactor, inputFile);

    %carrega dados de entrada
    loadedMatrix = load(inputFile);
    transitionMatrix = spconvert(loadedMatrix);

    %identifica numero de topicos na matriz de entrada
    numTopics = max(size(transitionMatrix));

    %torna a matriz quadrada
    [numRows, numColumns] = size(transitionMatrix);
    if [ (numRows ~= numTopics) || (numColumns ~= numTopics) ]
	transitionMatrix(numTopics,numTopics) = 0.0;
    end

    %remove arestas 'ruidosas entre topicos': assumimos que uma aresta representa um ruido se ela possui uma probabilidade menor que a aleatoria para o grafo de entrada
    % essa probabilidade é decomposta em duas etapas: probabilidade esperada para qualquer origem no grafo voltar para ela mesma e probabilidade de uma vez que saiu escolher qualquer outro destino
    restartProbability = sum(diag(transitionMatrix))/numTopics;
    minConnectionProbability = (1 - restartProbability) * 1/(numTopics-1);

    for i= 1:numTopics,
	for j= 1:numTopics,
		if [ transitionMatrix(i,j) <= minConnectionProbability ]
			transitionMatrix(i,j) = 0;
		end
	end

	if [ sum(transitionMatrix(i,:)) <= transitionMatrix(i,i) ]
		for j= 1:numTopics,
			if [ j ~= i ]
				transitionMatrix(i,j) = (1-transitionMatrix(i,i)) * 1/(numTopics-1);
			end
		end
	else
		norm = sum(transitionMatrix(i,:));
		for j= 1:numTopics,
				transitionMatrix(i,j) = transitionMatrix(i,j)/norm;
		end
	end
    end
			
    %gera matriz irredutivel
    irreducibleMatrix = dampFactor*transitionMatrix + ( ((1.0 - dampFactor) * (1.0/numTopics)) * ones(numTopics,numTopics) );



