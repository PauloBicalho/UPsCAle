function multiplicativeMethod(inputFile, maxItr, numFactors, outputDir);

%inicia contagem de tempo de carregamento e pre-processamento dos dados
tic;

%carrega dados de entrada
loadedMatrix = load(inputFile);
sparseMatrix = spconvert(loadedMatrix);

[numRows, numColumns] = size(sparseMatrix);

%obtem matrizes W e H randomicas
RandStream.setDefaultStream(RandStream('mt19937ar','seed',sum(100*clock)));
W = rand(numRows, numFactors);
H = rand(numFactors, numColumns);

residual = Inf;
epsilon = 0.000000001;

for itr = 1:maxItr, 

     H = H .* (W' * sparseMatrix) ./ ((W'*W)*H + epsilon );
     W = W .* (sparseMatrix * H') ./ (W*(H*H') + epsilon );

    [W] = normalize(W);
    [H] = normalize(H);
end

%imprime residual
%approximation = W * H;
%residual =norm(sparseMatrix-approximation,'fro')

%abre arquivo de saida
outputFileName = strcat(outputDir,'basis.txt');
outputFile = fopen(outputFileName, 'w');

%escreve saida em arquivo de saida
for i= 1:numRows,
   for j= 1:numFactors,
	  fprintf(outputFile,'%g ', W(i, j));
   end
   fprintf(outputFile,'\n');
end

%fecha arquivo
fclose(outputFile);

%abre arquivo de saida
outputFileName = strcat(outputDir,'coordinates.txt');
outputFile = fopen(outputFileName, 'w');

%escreve saida em arquivo de saida
for i= 1:numFactors,
   for j= 1:numColumns,
	  fprintf(outputFile,'%g ', H(i, j));
   end
   fprintf(outputFile,'\n');
end

%fecha arquivo
fclose(outputFile);

function [xnorm] = normalize(x)
	xmin = min(x(:));
	xmax = max(x(:));
	if xmin == xmax
	    % Constant matrix -- I choose to warn and return a NaN matrix
	    warning('normalization:constantMatrix', 'Cannot normalize a constant matrix to the range [0, 1].');
	    xnorm = nan(size(x));
	else
	    xnorm = (x-xmin) ./ (xmax-xmin);
	end

