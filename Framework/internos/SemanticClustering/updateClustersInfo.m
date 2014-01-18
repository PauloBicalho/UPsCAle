function [mapTopics, clusterAssignments] = updateClustersInfo(selectedTopic1, selectedTopic2, initialNumTopics, newTopicId, mapTopics, clusterAssignments)
	if( selectedTopic1 > initialNumTopics )
		selectedTopic1 = mapTopics(selectedTopic1 - initialNumTopics);
	end
	
	if( selectedTopic2 > initialNumTopics)
		selectedTopic2 = mapTopics(selectedTopic2 - initialNumTopics);
	end

	if( selectedTopic1 > selectedTopic2 )
		mapTopics(newTopicId - initialNumTopics) = selectedTopic1;
		clusterAssignments(selectedTopic2,:) = clusterAssignments(selectedTopic2,:) + clusterAssignments(selectedTopic1,:); 
	else
		mapTopics(newTopicId - initialNumTopics) = selectedTopic2;
		clusterAssignments(selectedTopic1,:) = clusterAssignments(selectedTopic1,:) + clusterAssignments(selectedTopic2,:); 
	end

