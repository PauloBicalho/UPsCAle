// OrganizeBaseGisele.cpp : Defines the entry point for the console application.
//

//#include "stdafx.h"

#include <cassert>
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

	if(argc != 6)
	{
		cout<<"Erro no número de parametros"<<endl;
		cout<<"<basis> <base> <tweets_grupos> <clusterHierarchy> <diretorio_saida>"<<endl;
		exit(1);
	}
	string arquivoEntrada = argv[1];
	
	fstream pFile;
	
	pFile.open(arquivoEntrada.c_str(),fstream::in | fstream::out | fstream::app);
	
	string line;
	
	vector<string> dados;
	vector<double> dados2;
	vector< vector<double> > dadosTotais;
	getline(pFile,line);
	
	boost::trim(line);
	if(line.size()>2)
	{	
		boost::split(dados,line,boost::is_any_of(" "));			
	}			
	else
	{
			cout<<"Erro de leitura"<<endl;
			exit(1);
	}		

	int size = dados.size();
	dados2.resize(size);
	float random = (double) 1/size;
	//Armazena as probabilidades de cada documento em relação aos tópicos.
	while(!pFile.eof())
	{
		float totalProb = 0;
		for(int i=0; i<size; i++)
		{
			try
			{
				dados2[i] = boost::lexical_cast<double> (dados[i]);
			} 
			catch( boost::bad_lexical_cast const& ) 
			{				
				dados2[i] = 0;
			}
			totalProb += dados2[i];
		}
	
		float norm;
		for(int i=0; i<size; i++)
		{
			norm = (float) dados2[i]/totalProb;
			if(norm > random)
				dados2[i] = norm;
			else
				dados2[i] = 0;
		}
		//armazena as probabilidades de cada documento pertencer a um determinado tópico 
		dadosTotais.push_back(dados2);

		getline(pFile,line);
		boost::trim(line);
		if(line.size()>2)
		{	
			boost::split(dados,line,boost::is_any_of(" "));				
		}		
		else
			continue;				

	}

	pFile.close();

	cout<<dadosTotais.size()<<" "<<dadosTotais[0].size()<<endl;

	string entrada = argv[2];

	fstream pEntr;

	map<string,int> usuarioDoc;
	map<string, int>::iterator it;

	//abri o arquivo de entrada da base e pega o id do usuário e o id do documento.					
	pEntr.open(entrada.c_str(),fstream::in | fstream::out | fstream::app);
	
	int usuario; 
	string documento;	
	while(!pEntr.eof())
	{
		getline(pEntr,line);
		boost::trim(line);
		if(line.size()>2)
		{	
			boost::split(dados,line,boost::is_any_of("\t"));				

		}	
		else
			continue;		
		try
		{
			usuario = boost::lexical_cast<int> (dados[0]);
			documento = dados[1];
		}
		catch( boost::bad_lexical_cast const& ) 
		{
			continue;
		}
		it=usuarioDoc.find(documento);
		if(it == usuarioDoc.end())
		{
			usuarioDoc[documento] = usuario;
//			cout<<documento<<" "<<usuario<<endl;
		}
		else
		{	

		}		

	}
	pEntr.close();
	cout<<usuarioDoc.size()<<endl;




	string tweets_grupos = argv[3];


	fstream pTweet;
	pTweet.open(tweets_grupos.c_str(),fstream::in | fstream::out | fstream::app);

	map<int,int> usuarios;
	map<int, int>::iterator it2;

	vector< vector<double> > usuariosTopicos;
	string idDocument;
	//verifica os ids dos documentos.
	int count = 0;
	while(!pTweet.eof())
	{
		getline(pTweet,line);
		boost::trim(line);
	
		if(line.size()>2)
		{	
			boost::split(dados,line,boost::is_any_of("\t"));				
		}
		else
			break;		

		idDocument = dados[0];
		
		it2 = usuarios.find(usuarioDoc[idDocument]);
		
		if(it2 == usuarios.end())
		{
			usuarios[usuarioDoc[idDocument] ] = usuarios.size();
			usuariosTopicos.push_back(dadosTotais[count]);
		}
		else
		{	
			for(int i =0; i<size; i++)
				usuariosTopicos[it2->second][i]+= dadosTotais[count][i];
		}
		
		count++;
		
	}

	cout<<usuariosTopicos.size()<<endl;
	for(int j =0; j<usuariosTopicos.size(); j++)	
	{
		double norm = 0;
		int size = usuariosTopicos[j].size();
		for(int i =0; i<size; i++)
		{	
			norm+=usuariosTopicos[j][i];
		}	
		cout<<norm<<endl;
		for(int i =0; i<size; i++)	
			usuariosTopicos[j][i] = (double)usuariosTopicos[j][i]/norm;	
	}

	cout<<"Passei aqui"<<endl;
/*	string saida = argv[4];
	saida+="/usuariosTopicos";
	ofstream  outFile(saida.c_str());
	int j;
	for (j=0, it2=usuarios.begin(); it2!=usuarios.end(); ++it2, j++)
	{	
		outFile<< it2->first<<" ";
		for(int i =0; i<usuariosTopicos[j].size(); i++)	
		   outFile<< usuariosTopicos[j][i]<<" ";	
		outFile<< endl;
	}

	cout<<usuariosTopicos.size()<<endl;
*/
		
	string topics = argv[4];
	fstream pTopics;
	pTopics.open(topics.c_str(),fstream::in | fstream::out | fstream::app);

	vector<string> dados3;

	map<string, int> topicsHierarchy;
	int label = 0;
	while(!pTopics.eof())
	{
		getline(pTopics,line);
		boost::trim(line);
		if(line.size()>2)
		{	
			boost::split(dados,line,boost::is_any_of("\t"));				
		}
		else
			continue;
		//lê todos os tópicos do nível 0, seus filhos e suas folhas.
		if(dados[0] == "0")	
		{
                        topicsHierarchy[dados[1]] = label;

			boost::split(dados3,dados[2],boost::is_any_of(","));
			for(int i =0; i<dados3.size(); i++)
				topicsHierarchy[dados3[i]] = label; 				
			boost::split(dados3,dados[3],boost::is_any_of(","));
			for(int i =0; i<dados3.size(); i++)
				topicsHierarchy[dados3[i]] = label; 				
			label++;
		}
		else//lê o restante dos níveis.
		{
			boost::split(dados3,dados[2],boost::is_any_of(","));
                        for(int i =0; i<dados3.size(); i++)
                                topicsHierarchy[dados3[i]] = topicsHierarchy[dados[1]];
                        boost::split(dados3,dados[3],boost::is_any_of(","));
                        for(int i =0; i<dados3.size(); i++)
                                topicsHierarchy[dados3[i]] = topicsHierarchy[dados[1]];
		}		
	}


/*	map<string, int>::iterator it3;

	for (it3=topicsHierarchy.begin(); it3!=topicsHierarchy.end(); ++it3)
        {       
                cout<<it3->first<<" "<<it3->second<<endl;
        }*/


	string saida = argv[5];
        saida+="/usuariosTopicos";
        ofstream  outFile(saida.c_str());

	vector<double> probTopic(label,0);
	vector<double> aux2(label,0);
	string aux;
	for(int j =0 ; j< usuariosTopicos.size(); j++)
	{
		for(int i =0 ; i< usuariosTopicos[j].size(); i++)
        	{	
			aux = boost::lexical_cast<string> (i);
			probTopic[topicsHierarchy[aux]]+= usuariosTopicos[j][i];
		}
		
		for( int k = 0; k<label;k++)
		{
			outFile<< probTopic[k]<<" ";
		}
		outFile<<endl;
		probTopic = aux2;
	}
	outFile.close();
	return 0;

}


