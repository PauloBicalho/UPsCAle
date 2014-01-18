function mergeTopics(dampFactor, inputFile, outputDir)

%inicia contagem de tempo de carregamento e pre-processamento dos dados
tic;

  [irreducibleMatrix, numTopics] = loadTransitionMatrix(dampFactor, inputFile);

%finaliza tempo de pre-processamento dos dados
preProcessingTime=toc;

% abre arquivos de saida
outputFileTopics = strcat(outputDir,'clusteringMergedTopics.txt');
outputFileTopics = fopen(outputFileTopics, 'w');
outputFileWeights = strcat(outputDir,'clusteringTopicWeights.txt');
outputFileWeights = fopen(outputFileWeights, 'w');

%seta variaveis estaticas
epsilon=0.00001;

%inicializa estruturas para manter mapeamento de indices dos topicos
finalNumTopics = numTopics;
for i= 1:numTopics,
	topicIndexes(i) = i;
	mapIndexTopic(i) = i;
end;

%inicia contagem de tempo do agrupamento
processingTime = 0.0;
tic;

 %gera probabilidades de alcançar topicos em numHops iterações do randomWalk
randomWalkMatrix = irreducibleMatrix;
numHops = getNetworkDiameter(numTopics,randomWalkMatrix);
for i= 1:(numHops-1),
    randomWalkMatrix = randomWalkMatrix * irreducibleMatrix;
end;

%define probabilidade de sair de um topico durante a navegacao no grafo
%tal probabilidade considera a probabilidade esperada de se sair do topico atual e a probabilidade de ir aleatoriamente para qualquer outro topico
leavingProbability = (1 - sum(diag(irreducibleMatrix))/numTopics);

% calcula probabilidade minima necessaria para a juncao de dois topicos distintos: 
% tal valor é definido como o valor que um pulo randômico teria na base analisada
[meanNumberOfLinks] = getNumLinks(numTopics, irreducibleMatrix);
%minProbability = floor((leavingProbability * 1/(meanNumberOfLinks)) * 100)/100;
minProbability = leavingProbability * 1/(meanNumberOfLinks);

topicSize = ones(2*numTopics,1);
originalNumTopics = numTopics;

%itera enquanto o numero de topicos resultantes for maior que 1
while (numTopics > 1)

      currentIndex = 1;
      [selectedRows, selectedColumns, maxProbabilities] = selectBestTopicPair1(numTopics, randomWalkMatrix, topicIndexes, topicSize);
      while ( (currentIndex < numTopics) && ( maxProbabilities(currentIndex) > minProbability) )
      		%identifica proximo par de topicos a serem aglutinados
		selectedRow = mapIndexTopic( selectedRows(currentIndex) );
		selectedColumn = mapIndexTopic( selectedColumns(currentIndex) );

	      	%recupera o primeiro autovetor da matriz irredutível
		[stationaryProbabilities] = getStationaryDistribution(dampFactor, epsilon, numTopics, irreducibleMatrix);

		%para contagem de tempo
      		partialTime=toc;
      		processingTime=processingTime + partialTime;

      		%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      		%imprime informacoes em arquivo de saida

      		fprintf(outputFileTopics,'%g\t%g\t%g\t%g\t%g\n', topicIndexes(selectedRow), topicIndexes(selectedColumn), maxProbabilities(currentIndex), minProbability, leavingProbability);

      		for i= 1:(numTopics-2),
	     		diff = 0;
	     		index = topicIndexes(i);
			if( index >= topicIndexes(selectedRow) )
				diff = diff + 1;
	     		end
	     		if( index >= topicIndexes(selectedColumn) )
				diff = diff + 1;
	     		end

	     		index = i + diff;
	     		while( index <= numTopics )
	     	  		if [ ( topicIndexes(index) ~= topicIndexes(selectedRow) ) && ( topicIndexes(index) ~= topicIndexes(selectedColumn) ) ]
					break;
		  		end

		  		index = index + 1;
	     		end
	     		if [ index <= numTopics ]
		     		topicIndexes(i) = topicIndexes(index);
		     		mapIndexTopic( topicIndexes(index) ) = i; 
	     		end
      		end
      		finalNumTopics = finalNumTopics + 1;
      		topicIndexes(numTopics-1) = finalNumTopics;
		topicSize( topicIndexes(numTopics-1) ) = topicSize( topicIndexes(selectedRow) ) + topicSize( topicIndexes(selectedColumn) );
      		mapIndexTopic( finalNumTopics ) = numTopics - 1;

      		fprintf(outputFileWeights,'%g', numTopics);
      		for i=1:numTopics,
	    		fprintf(outputFileWeights,' %g',stationaryProbabilities(i));
      		end
      		fprintf(outputFileWeights,'\n');

      		%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

      		%retoma contagem de tempo
      		tic;
 
      		%inicializa nova matriz com zeros
      		newMatrix = zeros(numTopics -1, numTopics -1);
      		mapNewOldIndex = zeros(numTopics -1);
      
      		%atualiza probabilidades de transições entre tópicos não afetados pela fusão
      		validRowIndex = 0;
      		for i= 1:numTopics,
	    		if [ (i ~= selectedRow) && (i ~= selectedColumn) ]
	    
				validRowIndex = validRowIndex + 1;
				mapNewOldIndex(validRowIndex) = i;
				validColumnIndex = validRowIndex - 1;
				for j= i:numTopics,
		    			if [ (j ~= selectedRow) && (j ~= selectedColumn) ]
		    
			 			validColumnIndex = validColumnIndex + 1;
			 			newMatrix(validRowIndex,validColumnIndex) = irreducibleMatrix(i,j);
						newMatrix(validColumnIndex,validRowIndex) = irreducibleMatrix(j,i);
		    			end 
				end
	    		end
      		end

      		%atualiza numero de topicos da matriz
      		numTopics = numTopics - 1;

      		%adiciona novo topico resultante da fusão entre dois outros como ultima linha da nova matriz
      		for i= 1:(numTopics-1),
	    		newMatrix(i,numTopics) = irreducibleMatrix( mapNewOldIndex(i) , selectedRow) + irreducibleMatrix( mapNewOldIndex(i) , selectedColumn);
	    		newMatrix(numTopics,i) = irreducibleMatrix( selectedRow, mapNewOldIndex(i)) * stationaryProbabilities(selectedRow)/(stationaryProbabilities(selectedRow) + stationaryProbabilities(selectedColumn)) + irreducibleMatrix( selectedColumn, mapNewOldIndex(i)) * stationaryProbabilities(selectedColumn)/(stationaryProbabilities(selectedRow) + stationaryProbabilities(selectedColumn));

      		end
      
      		%atualiza probabilidade do novo topico ficar nele mesmo
      		newMatrix(numTopics,numTopics) = (irreducibleMatrix(selectedRow,selectedRow) + irreducibleMatrix(selectedRow,selectedColumn)) * stationaryProbabilities(selectedRow)/(stationaryProbabilities(selectedRow) + stationaryProbabilities(selectedColumn)) + (irreducibleMatrix(selectedColumn,selectedColumn) + irreducibleMatrix(selectedColumn,selectedRow)) * stationaryProbabilities(selectedColumn)/(stationaryProbabilities(selectedRow) + stationaryProbabilities(selectedColumn));      

      		%atualiza matriz irredutivel
      		newMatrix(isnan(newMatrix)) = 0;  
      		irreducibleMatrix = newMatrix;


      		currentIndex = currentIndex + 1;

      end

      %gera probabilidades de alcançar topicos em numHops iterações do randomWalk
      randomWalkMatrix = irreducibleMatrix;
      numHops = getNetworkDiameter(numTopics,randomWalkMatrix);

      for i= 1:(numHops-1),
		randomWalkMatrix = randomWalkMatrix * irreducibleMatrix;
      end

      %define probabilidade de sair de um topico durante a navegacao no grafo
      %tal probabilidade considera a probabilidade esperada de se sair do topico atual e a probabilidade de ir aleatoriamente para qualquer outro topico
      leavingProbability = (1 - sum(diag(irreducibleMatrix))/numTopics);

      % calcula probabilidade minima necessaria para a juncao de dois topicos distintos: 
      % tal valor é definido como o valor que um pulo randômico teria na base analisada
      [meanNumberOfLinks] = getNumLinks(numTopics, irreducibleMatrix);
      minProbability = numTopics/originalNumTopics * leavingProbability * 1/(meanNumberOfLinks);
      %minProbability =  leavingProbability * 1/(meanNumberOfLinks);

      if [ currentIndex == 1]
	     break;
      end
end 

%finaliza contagem de tempo
partialTime=toc;
processingTime=processingTime + partialTime;

%imprime distribuicao final no arquivo de saida
[stationaryProbabilities] = getStationaryDistribution(dampFactor, epsilon, numTopics, irreducibleMatrix);
fprintf(outputFileWeights,'%g', numTopics);
for i=1:numTopics,
	fprintf(outputFileWeights,' %g',stationaryProbabilities(i));
end
fprintf(outputFileWeights,'\n');

%fecha arquivos de saida
fclose(outputFileTopics);
fclose(outputFileWeights);

% abre arquivo de saida
outputFile = strcat(outputDir,'clusteringTimes.txt');
outputFile = fopen(outputFile, 'w');

%escreve pagerank em arquivo de saida
fprintf(outputFile,'%g\t%g\n', preProcessingTime, processingTime);

%fecha arquivo
fclose(outputFile);

memoryInfo = whos;

% abre arquivo de saida
outputFile = strcat(outputDir,'clusteringMemoryInfo.txt');
outputFile = fopen(outputFile, 'w');

%escreve pagerank em arquivo de saida
for i= 1:length(memoryInfo),
     fprintf(outputFile,'%s\t%u\n', getfield(memoryInfo(i), 'name'), getfield(memoryInfo(i), 'bytes'));
end;

%fecha arquivo
fclose(outputFile);

% abre arquivo de saida
outputFile = strcat(outputDir,'clusteringTransitionMatrix.txt');
outputFile = fopen(outputFile, 'w');

%escreve pagerank em arquivo de saida
for i= 1:numTopics,
    for j= 1:numTopics,
	if [irreducibleMatrix(i,j) > 0 ] 
		fprintf(outputFile,'%g %g %g\n', topicIndexes(i), topicIndexes(j), irreducibleMatrix(i,j));
	end
    end
end

%fecha arquivo
fclose(outputFile);


