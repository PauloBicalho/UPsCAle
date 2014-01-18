#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
#include <iomanip>
#include <dirent.h>
#include <boost/format.hpp>
#include <map>
#include <boost/algorithm/string.hpp>

using namespace std;


//parametros: <basis> <base> <tweets_grupos> <diretorio_saida>
int main(int argc, char* argv[])
{
	fstream pFile;

	string arquivoEntrada = argv[1];
	pFile.open(arquivoEntrada.c_str(),fstream::in | fstream::out | fstream::app);
	string line;
	vector<string> dados;
	vector<string> dados2;
//	vector< vector<double> > dadosTotais;
	
	map<string,int> docTopicos;
        map<string, int>::iterator it;

	 while(!pFile.eof())
	{
		
		getline(pFile,line);
//		boost::trim(line);
//		cout<<line<<endl;
		if(line.size()>2)
		{
			boost::split(dados,line,boost::is_any_of("\t"));
		}
		else
		{
			break;
		}
		
		boost::split(dados2,dados[1],boost::is_any_of(","));
		//cout<<dados[1]<<endl;		
		
		for (int i =0; i<  dados2.size(); i++)
		{
			it = docTopicos.find(dados2[i]);
			if(it == docTopicos.end())
			{
                            docTopicos[dados2[i]] = 1;
//			    cout<<dados2[i]<<endl;	
                        }			
			else
			{
			     docTopicos[dados2[i]] = docTopicos[dados2[i]] + 1;
//			     cout<<dados2[i]<<endl;	
			}
		}
		
	}
	string saida = argv[2];
        ofstream  outFile(saida.c_str());
	map<string, int>::iterator it2;
        for (it2=docTopicos.begin(); it2!=docTopicos.end(); ++it2)
        {       
		outFile<< it2->first<<" "<<it2->second<<endl;
        }

	return 0;

		
}