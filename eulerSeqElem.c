#ifndef EULERSEQELEM
#define EULERSEQELEM

#include <stdio.h>
#include "graph.h"

struct eulerSeqElem{
  struct vertice from;
  struct vertice to;
};

void printSeqElem(struct eulerSeqElem* A){
  if ( A ) printf("%u %u,", A->from.id,A->to.id);
  else printf("NULL");
}

#endif
