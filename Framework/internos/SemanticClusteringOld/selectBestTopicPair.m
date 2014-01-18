function [selectedRow, selectedColumn, maxProbability] = selectBestTopicPair(numTopics, matrix)

      %zera diagonais para evitar de retorná-las
      for i= 1:numTopics,

	  for j= (i+1):numTopics,
		temporaryMatrix(i,j) = ( (1.0 - matrix(i,i)) * matrix(i,j) + (1.0 - matrix(j,j)) * matrix(j,i) )/2;
		temporaryMatrix(j,i) = temporaryMatrix(i,j);
	  end

	  temporaryMatrix(i,i) = 0;
      end

      % identifica topicos com maior probabilidade de serem alcançados a partir de cada topico
      [maxProbabilities,columnIndices] = max(temporaryMatrix');

      % identifica o par de topicos a ser aglutinado (i.e., o par de topicos com maior probabilidade de serem alcancaveis). Neste processo, a linha é aglutinada à coluna
      [maxProbability,selectedRow] = max(maxProbabilities);
      selectedColumn = columnIndices(selectedRow);
