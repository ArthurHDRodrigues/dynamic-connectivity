#ifndef EULERSEQELEM
#define EULERSEQELEM

#include "graph.h"

struct eulerSeqElem{
  struct vertice from;
  struct vertice to;
};

void printSeqElem(struct eulerSeqElem*A);

#endif
