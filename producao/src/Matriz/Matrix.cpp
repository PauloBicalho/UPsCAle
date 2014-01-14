#include "Matrix.h"
#include <iostream>
#include <cstdlib>
#include <cstdio>


Matrix::Matrix(char * database, char * words, int columnStart, int columnEnd){

  FILE * fWords = fopen(words, "r");

  if( fWords == NULL){
    perror("Error opening words file: ");
    exit(1);
  }

  char wline [100];
  char word[100];

  string w;

  int index = 0;
  while( fgets(wline, 100, fWords) != NULL ){

    sscanf(wline, "%s ", word);
    w = string (word);
    
    wordToId[w] = index;
    index++;
  }

  fclose(fWords);
  FILE * fin = fopen(database,"r");
  
  if( fWords == NULL){
    perror("Error opening database file: ");
    exit(1);
  }

  char line [1000];
  int lineCounter = 0;

  while( fgets(line, 1000, fin) != NULL ){
    this->values.push_back( *(new map< int, int >) );

    char * aux = line;
    int i = -1;
    while( sscanf(aux, "%s ", word) != EOF){
      w = string (word);
      
      i++;
      if( i < columnStart ){
        aux = aux + (int) w.size() + 1;
        continue;
      }

      if( i > columnEnd )
        break;


      cout << w << " ";

      int wId = wordToId[w];
      if( this->values[lineCounter].find(wId) == this->values[lineCounter].end() )
        this->values[lineCounter][wId] = 1;
      else
        this->values[lineCounter][wId]++;

      aux = aux + (int) w.size() + 1;
    }

    cout << "\n";
    
    lineCounter++;
  }

}

void Matrix::print(){

  for( int i=0; i < this->values.size(); i++){
    map<int, int>::iterator it;
    for(it = this->values[i].begin(); it != this->values[i].end(); ++it){
      cout << i << "-" << it->first << " " << it->second << "\n";
    }
  }
}


