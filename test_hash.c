#include <stdio.h>
#include <stdlib.h>
#include "hash.h"
#include "eulerSequence.h"


int main (){
  double x = 1.7878786666;
  
  struct vertice v;
  v.id = 69;
  
  struct Treap treap = eulerSeq(v, v);
  
  struct hash_node* hash = createHash ( &treap , 10 );
  
  printHash(hash);
  
  printf("x: %f\n", x);
  
  printf("x: %f\n", x-((long)x ));
  return 0;
}
