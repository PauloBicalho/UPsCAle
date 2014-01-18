function [selectedRows, selectedColumns, maxProbabilities] = selectBestTopicPair1(numTopics, matrix, topicIndexes, topicSize)

      matrixSize = numTopics * numTopics;
      dirtyTopics = zeros(numTopics);
      maxProbabilities = zeros(numTopics);
      selectedRows = zeros(numTopics);
      selectedColumns = zeros(numTopics);
      temporaryMatrix = zeros(numTopics, numTopics);

      %zera diagonais para evitar de retorná-las
      for i= 1:numTopics,

	  startIndex = (i-1) * numTopics + 1;
	  for j=(i+1):numTopics,

		transitionProbability = (matrix(i,j) + matrix(j,i))/2;
		relevance1 = topicSize( topicIndexes(i) );
		relevance2 = topicSize( topicIndexes(j) );

		if [ relevance1 < relevance2 ]
			penality = 1.0/relevance1;
		else
			penality = 1.0/relevance2;
		end

		temporaryMatrix(i,j) = penality * transitionProbability;
		startIndex = startIndex + 1;
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

