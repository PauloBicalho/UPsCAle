  function [selectedRows, selectedColumns, maxProbabilities] = selectBestTopicPairMean(numTopics, matrix, topicIndexes, clusterAssignment, mapTopics, originalNumTopics, alpha, minProbability, maxCohesion, transitionMatrix)

      matrixSize = numTopics * numTopics;
      dirtyTopics = zeros(numTopics);
      maxProbabilities = zeros(numTopics);
      selectedRows = zeros(numTopics);
      selectedColumns = zeros(numTopics);
      temporaryMatrix = zeros(numTopics, numTopics);

      %zera diagonais para evitar de retorná-las
	numTopics	
      for i=1:numTopics,

	  topic1 = topicIndexes(i);
	  if [ topic1 > originalNumTopics ]
		topic1 = mapTopics(topic1 - originalNumTopics);
	  end

	  for j=(i+1):numTopics,

		topic2 = topicIndexes(j);
		if [ topic2 > originalNumTopics ]
			topic2 = mapTopics(topic2 - originalNumTopics);
		end

		resultingCluster = clusterAssignment(topic1,:) + clusterAssignment(topic2,:);
		numFactors = sum(resultingCluster);
		auxilaryMatrix = resultingCluster' * resultingCluster;
		auxilaryMatrix = auxilaryMatrix - diag( resultingCluster );
		resultingVector = diag(transitionMatrix * auxilaryMatrix');

		meanCohesion = sum(resultingVector)/( numFactors*(numFactors-1) );
		maxCohesion = 1.0/numFactors;
		deltaCohesion = (meanCohesion - maxCohesion)/maxCohesion;

		transitionProbability = (matrix(i,j) + matrix(j,i))/2;
		deltaUnicity = (transitionProbability - minProbability)/minProbability;

		temporaryMatrix(i,j) = alpha*deltaCohesion + (1.0 - alpha)*deltaUnicity;
		%fprintf('%g  %g  %g  %g  %g  %g  %g  %g  %g\n', i, j, matrix(i,j), matrix(j,i), transitionProbability, deltaCohesion, deltaUnicity, alpha, temporaryMatrix(i,j));
	  end

      end

      probabilities = reshape(temporaryMatrix',matrixSize,1);
      [sortedProbabilities, indices] = sort(probabilities, 'descend');

      index = 1;
      for i= 1:matrixSize,
		if [ sortedProbabilities(i) == 0 ]
			break;
		end

		selectedRow = floor(indices(i)/numTopics) + 1;
		selectedColumn = mod(indices(i),numTopics);
		if [ selectedColumn == 0 ]
			selectedRow = selectedRow - 1;
			selectedColumn = numTopics;
		end

		if [ (dirtyTopics(selectedColumn) ~= 1) && (dirtyTopics(selectedRow) ~= 1 ) ]
			selectedRows(index) = topicIndexes(selectedRow);
			selectedColumns(index) = topicIndexes(selectedColumn);
			maxProbabilities(index) = sortedProbabilities(i);
			index = index + 1;

			dirtyTopics(selectedColumn) = 1;
			dirtyTopics(selectedRow) = 1;	
		end

      end

