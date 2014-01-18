function [rankVector] = getStationaryDistribution(dampFactor, epsilon, numTopics, transitionMatrix);

%identifica numero de paginas na matriz de entrada
numTopics = max(size(transitionMatrix));

%gera vetor de 1's
vectorOfOnes = ones(1,numTopics);

%inicializa variaveis utilizadas nas iteracoes
numIteractions=0;
residual=1;
rankVector = 1/numTopics * vectorOfOnes;

%gera o pagerank iterativamente
while (residual >= epsilon) 
     prevRankVector = rankVector;
     auxilaryVector = dampFactor * rankVector * transitionMatrix;
     beta = 1 - norm(auxilaryVector,1);
     rankVector = auxilaryVector + beta * 1/numTopics * vectorOfOnes;
     
     residual = norm(rankVector - prevRankVector,1);
  
     numIteractions = numIteractions + 1;
     residualVector(numIteractions) = residual;
end
