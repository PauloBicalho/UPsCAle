function getNumEigenVectors(inputFile, maxSize, minCoverage, outputFileName);

% abre arquivo de saida
outputFile = fopen(outputFileName, 'w');

eigenvalues = load(inputFile);
eigenvalues = eigenvalues .^ 2;
[numEigen,trash] = size(eigenvalues);

X = 1:numEigen;
X = X';

regression = polyfit(X, log(eigenvalues), 1);

X = 1:maxSize;
X = X';

predictions = polyval(regression, X);
%coefficients = glmfit(X, eigenvalues, 'poisson', 'link', 'log');
%predictions = glmval(coefficients, X,'reciprocal');

for eigenv= 1:maxSize,
	if [ eigenv <= numEigen ]
		if [ eigenvalues(eigenv) < 1.0 ]
			eigenvalues(eigenv) = 0.0;
		end
	else
		if [ predictions(eigenv) < 1.0 ]
			predictions(eigenv) = 0.0;
		end
	end
end

sumEigenvectors = sum(eigenvalues) + sum(predictions(numEigen+1:maxSize));

accumulator = 0;
numEigenv = 1;
for eigenv= 1:maxSize,
      if [ accumulator >= minCoverage | predictions(eigenv) < 1.0 ]
	  break
      end

      if [ eigenv > numEigen ]      
	      accumulator =  accumulator + predictions(eigenv) / sumEigenvectors;
      else
	      accumulator =  accumulator + eigenvalues(eigenv) / sumEigenvectors;
      end
      numEigenv = eigenv;
end

fprintf(outputFile, '%d', numEigenv);

%fecha arquivo
fclose(outputFile);
