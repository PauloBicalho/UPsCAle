#include <iostream>

#include "Matrix.h"

int main(int argc, char * argv[]){

  Matrix m ("testIn/db.txt", "testIn/words.txt", 2, 100000);
  m.print();


  return 0;
}
