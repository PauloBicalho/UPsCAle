function [meanNumberOfLinks] = getNumLinks(numTopics, matrix)

    numLinks = 0;
    restartProbability = sum(diag(matrix))/numTopics;
    minConnectionProbability = (1 - restartProbability) * 1/(numTopics-1);

    for i= 1:numTopics,    

	for j= 1:numTopics,
	    if [ (i ~= j) && (matrix(i,j) > minConnectionProbability) ]
		numLinks = numLinks + 1;
	    end

	end	
    end

    meanNumberOfLinks = numLinks/numTopics;

