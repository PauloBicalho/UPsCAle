function [irreducibleMatrix, numTopics] = identify_topk_items(arquivo_entrada, arquivo_saida, numSelected, nodeId);

    %carrega dados de entrada
    loadedMatrix = load(arquivo_entrada);
    [num_rows, num_columns] = size(loadedMatrix);
   
    [Q,RS,P] = qr(loadedMatrix);
    p = [1:num_columns]*P;
    topKItems = p(1:numSelected);

    % abre arquivo de saida
    outputFile = fopen(arquivo_saida, 'a');

    fprintf(outputFile,'%g\t', nodeId);
    for i= 1:numSelected,
	  fprintf(outputFile,'%g ', topKItems(i));
    end;
    fprintf(outputFile,'\n');

