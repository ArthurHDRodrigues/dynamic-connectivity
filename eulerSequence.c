#include <stdio.h>
#include <stdlib.h>
#include "eulerSequence.h"

/**************************************************\
 *        Euler Sequence e seus método            *
\**************************************************/

// struct eulerSeqElem declarado no início do arquivo para evitar erros...

void printSeq(struct Treap* treap){
  if(treap){
    if(treap->esq) printSeq(treap->esq);
    printSeqElem(&(treap->valor));
    if(treap->dir) printSeq(treap->dir);
  } else printf("NULL");
}

struct Treap eulerSeq( struct vertice from, struct vertice to){
  /* 
   * Retorna uma sequência que contém somente o elemento dado como parametro.
   */
  struct eulerSeqElem valor = {
  .from = from,
  .to = to,
  };
  return makeTree(valor);
}

struct Treap* find(struct Treap* node){
  /*
   * Retorna a raiz da árvore em que o nó 'node' se encontra
   */
  if ( node ){
    if ( node->parent ) return find(node->parent);
    return node;
  }
  return NULL;
}

/*
 * Order já está implementado
 */

struct Treap* slice(struct Treap** raiz, unsigned int K){
  /*
   * Recebe sequência raiz[1..n] e K
   * Retorna raiz[K+1..n] e, após a execução o ponteiro
   * raiz fica com raiz[1..K]
   */

  struct Treap* knode = search(*raiz, K);

  struct Treap* L=NULL;
  struct Treap* R=NULL;

  split(knode, &L, &R);

  *raiz = L;
  return R;
}

struct Treap* concatenate(struct Treap* nodeA, struct Treap* nodeB){
  /*
   * Recebe duas sequências Eulerianas e retorna a concatenação delas,
   * mantendo a propriedade de ser Eulerianas
   */
  
  return join(find(nodeA),find(nodeB));
}


void bringToFront(struct Treap* node){
  /*
   * Traz o elemento de sequência 'node' para o ínicio de sua sequência
   */
  unsigned int K = order(node);
  
  struct Treap* raiz = find(node);
  struct Treap* raizB = slice(&raiz, K-1);
  
  raiz = slice(&raiz, 1); // Remove a antiga raiz
  
  struct Treap* XX = NULL; 

  struct Treap* tmp = search(raizB, 1);
  
  if ( tmp ) {
     XX = malloc(sizeof(struct Treap));
    *XX = eulerSeq(tmp->valor.to, tmp->valor.to);
  }
  
  raiz = join(raizB,raiz);
  raiz = join(raiz,XX);
}
