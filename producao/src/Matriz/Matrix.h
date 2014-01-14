#ifndef MATRIX_H
#define MATRIX_H

#include <map>
#include <vector>
#include <string>

using namespace std;

class Matrix{
  public:

    Matrix(char * database, char * words, int columnStart, int columnEnd);
    ~Matrix(){;}

    void print();

  private:

    map<string, int> wordToId;
    vector< map<int, int> > values;

};



#endif // MATRIX_H
