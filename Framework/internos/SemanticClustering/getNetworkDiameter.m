function [diameter] = getNetworkDiameter(numTopics, matrix)

    restartProbability = sum(diag(matrix))/numTopics;
    minConnectionProbability = (1 - restartProbability) * 1/(numTopics-1);

    isolatedRows = zeros(numTopics);
    isolatedColumns = zeros(numTopics);
    fullMatrix = zeros(numTopics, numTopics);

    rowIndex = 0;
    selectedRow = 0;
    for i= 1:numTopics,    

        for j= 1:numTopics,
            if [ matrix(i,j) > minConnectionProbability ]
                fullMatrix(i,j) = 1;
            end

        end
    end

    sparseMatrix = sparse(fullMatrix);

    [distances] = dijk(sparseMatrix,[],[]);

    diameter = 1;
    for i= 1:numTopics,
	for j= 1:numTopics,
		if [ (distances(i,j) ~= Inf) && (distances(i,j) > diameter) ]
			diameter = distances(i,j);
		end
	end
    end

