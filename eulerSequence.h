#ifndef EULERSEQUENCE
#define EULERSEQUENCE

#include "graph.h"
#include "treaps.h"

struct Treap eulerSeq( struct vertice from, struct vertice to);
void printSeq(struct Treap* treap);
struct Treap* find(struct Treap* node);
struct Treap* slice(struct Treap** raiz, unsigned int K);
struct Treap* concatenate(struct Treap* raizA, struct Treap* raizB);
void bringToFront(struct Treap* node);
#endif
