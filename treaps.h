#ifndef TREAP
#define TREAP

#include "eulerSeqElem.h"

struct Treap{
  struct eulerSeqElem valor;         // Campo satélite 
  int prio;          // Chave para Heap
  unsigned int size; //Campo implicito usado para ABB
  struct Treap* esq;
  struct Treap* dir;
  struct Treap* parent;
  struct Treap* inv; //Endereço do arco inverso: se for vw.inv == wv
};


struct Treap makeTree(struct eulerSeqElem valor);

void printTreap(struct Treap* treap);

unsigned int getTreeSize(struct Treap* raiz);

struct Treap* search(struct Treap* raiz, unsigned int K);

unsigned int order(struct Treap* node);

void split(struct Treap* node, struct Treap** L, struct Treap** R);

struct Treap* join(struct Treap* raizA, struct Treap* raizB);

#endif
