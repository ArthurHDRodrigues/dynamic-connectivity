#ifndef DYN_FLOREST
#define DYN_FLOREST

struct dynamicForest{
  unsigned int n;        // Number of vertices in forest
  struct Treap* Forest;  // Vector of tree of size n dynamically allocated
};

struct dynamicForest createDynamicForest(unsigned int n);

int fconnected(struct dynamicForest* F, struct Treap* v, struct Treap* w);

void link (struct dynamicForest* F, struct Treap* v, struct Treap* w);

void cut (struct dynamicForest* F, struct Treap* vw);

#endif
