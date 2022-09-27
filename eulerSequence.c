#include <stdio.h>
#include <stdlib.h>
#include "treaps.h"

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

struct Treap* concatenate(struct Treap* raizA, struct Treap* raizB){
  /*
   * Recebe duas sequências Eulerianas e retorna a concatenação delas,
   * mantendo a propriedade de ser Eulerianas
   */
  struct Treap* AB = malloc(sizeof(struct Treap));
  struct Treap* BA = malloc(sizeof(struct Treap));
  struct Treap* AA = malloc(sizeof(struct Treap));
  
  //Pega último==primeiro elemento da sequência A
  struct Treap* A = search(raizA,1);
  struct Treap* B = search(raizB,1);
  
  *AA = eulerSeq(A->valor.to, A->valor.to);
  *AB = eulerSeq(A->valor.to, B->valor.to);
  *BA = eulerSeq(B->valor.to, A->valor.to);
  
  AB->inv = BA;
  BA->inv = AB;
  
  return join(join(join(join(raizA, AB),raizB),BA), AA);
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
