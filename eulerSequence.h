#ifndef EULERSEQUENCE
#define EULERSEQUENCE

#include "graph.h"
#include "treaps.h"

void printSeq(struct Treap* treap);

struct Treap eulerSeq( struct vertice from, struct vertice to);

struct Treap* find(struct Treap* node);

struct Treap* slice(struct Treap** raiz, unsigned int K);

struct Treap* concatenate(struct Treap* raizA, struct Treap* raizB);

void bringToFront(struct Treap* node);

#endif
