/*
 * Implementação de uma Floresta Dinamica
 * Para compilar: gcc -Wall treaps.c -o treaps
 */

#include <stdio.h>
#include <stdlib.h>

#include "graph.h"
#include "eulerSeqElem.h"

/**************************************************\
 *             Treap e seus métodos               *
\**************************************************/

struct Treap{
  struct eulerSeqElem valor;         // Campo satélite 
  int prio;          // Chave para Heap
  unsigned int size; //Campo implicito usado para ABB
  struct Treap* esq;
  struct Treap* dir;
  struct Treap* parent;
  struct Treap* inv; //Endereço do arco inverso: se for vw.inv == wv
};

struct Treap makeTree(struct eulerSeqElem valor){
  /*
   * Cria uma nova árvore, com apenas o elemento 'valor' e devolve sua raiz
   */
  struct Treap raiz = {
    .valor = valor,
    .prio = rand(),
    .size=1,
    .esq = NULL,
    .dir = NULL,
    .parent = NULL,
    .inv = NULL,
  };
  return raiz;
}

void printTreap(struct Treap* treap){
    if ( treap ){
      printSeqElem(&(treap->valor));
    } else printf("NULL");
}


unsigned int getTreeSize(struct Treap* raiz){
  if(raiz) return raiz->size;
  return 0;
}

struct Treap* search(struct Treap* raiz, unsigned int K){
  /* 
   * Retorna o K-ésimo elemento da sequência ou NULL, caso ele não exista
   */

  if ( raiz ){
    // Testa se K-esimo nó está na subárvore a esquerda
    if ( getTreeSize(raiz->esq) >= K ) return search(raiz->esq, K);

    // Testa se raiz é o K-esimo nó
    if ( K == getTreeSize(raiz->esq) + 1) return raiz;


    // Se não está na sub-árvore a esquerda nem é a raiz,
    // então tem que estar na subárvore a direita
    // Não tem problema se raiz->dir == NULL
    return search(raiz->dir, K-getTreeSize(raiz->esq)-1);
  }
  return NULL;
}; 


unsigned int order(struct Treap* node){
  /*
   * Retorna a posição do nó 'node' começando por 1;
   * Retorna 0 caso a árvore seja vazia.
   */
  if ( node ){
    unsigned int order_parent = 0;
    
    // Procura o descendente mais proximo que é filho a direta ou é a raiz
    struct Treap* tmp_node = node;
    while (tmp_node->parent && tmp_node == tmp_node->parent->esq  )
      tmp_node = tmp_node->parent;
      
    tmp_node = tmp_node->parent;
    
    if ( tmp_node )
      order_parent = order(tmp_node);
    return order_parent + getTreeSize(node->esq)+1;
  }
  return 0;
}

void split(struct Treap* node, struct Treap** L, struct Treap** R){
  /*
   * Recebe uma árvore 'node' (não necessariamente uma raiz)
   * e divide a árvore em 2, uma com os nós anteriores incluindo 'node'
   * e outra com os nós posteriores a 'node'.
   *
   * Após a chamada, L e R apontam para as duas árvores resultantes
   */
  
  if ( node ) {
    *L = node;
    *R = node->dir; //Pode ser NULL, não tem problemas!
    node->dir = NULL;
    
    // Atualiza o size de L; R já está com size correto
    (*L)->size = getTreeSize((*L)->esq) + getTreeSize((*L)->dir) + 1;

    
    // A cada iteração, vamos decidir se tmp_node->parent deve estar em L ou R
    // Invariantes de laço:
    //   - Após cada iteração temos tmp_node->parent==L ou tmp_node->parent==R
    //   - R->size e L->size estão corretos
    struct Treap* tmp_node = node;
    while ( tmp_node->parent ){
    
      if ( tmp_node->parent->dir == tmp_node ){

        // Se for filho a direita, tmp_node->parent fica em L
        tmp_node->parent->dir = *L;
	if ( *L ) (*L)->parent = tmp_node->parent;
	
        *L = tmp_node->parent;
        (*L)->size = getTreeSize((*L)->esq) + getTreeSize((*L)->dir) + 1;
      } else {
      
        // Se for filho a esquerda, tmp_node->parent fica em R
        tmp_node->parent->esq = *R;
        if ( *R ) (*R)->parent=tmp_node->parent;
	
	*R = tmp_node->parent;
	(*R)->size = getTreeSize((*R)->esq) + getTreeSize((*R)->dir) + 1;
      }
      tmp_node=tmp_node->parent; 
    }
    if (*L) (*L)->parent = NULL;
    if (*R) (*R)->parent = NULL;
  } else {
    // Se a árvore está vazia, garante que L e R estão definidos
    L = NULL;
    R = NULL;
  }
}

struct Treap* join(struct Treap* raizA, struct Treap* raizB){
  /*
   * Retorna um ponteiro para a raiz da árvore resultante
   * Assumimos que chaves de raizA < chaves de raizB
   */
   
  // Se uma for vazio, então retornamos a outra
  if ( !raizB ) return raizA;
  if ( !raizA ) return raizB;
  

  if ( raizA->prio > raizB->prio ){
    raizA->dir=join(raizA->dir, raizB);
    raizA->dir->parent = raizA;
    raizA->size=getTreeSize(raizA->esq) + getTreeSize(raizA->dir) + 1;
    return raizA;
  } else {
    raizB->esq=join(raizA, raizB->esq);
    raizB->esq->parent = raizB;
    raizB->size=getTreeSize(raizB->esq) + getTreeSize(raizB->dir) + 1;
    return raizB;
  }
};
