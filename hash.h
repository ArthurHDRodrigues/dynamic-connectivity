#ifndef __HASH
#define __HASH

#include "treaps.h"

#define GOLDEN_RATIO 0.6180339887498949

// (sqrt(5)-1)/2

struct hash_node{
  // hash é na verdade uma treap com campo explicito
  struct Treap* valor;         // Campo satélite 
  unsigned int size;
  int prio;           // Chave para Heap
  unsigned int index; //Campo explicito usado para ABB
  /*
   * index = (4n) * ((i*n+j)*A mod 1)
   * A = golden_ratio = (sqrt(5)-1)/2
   * n = size
   */
  struct hash_node* esq;
  struct hash_node* dir;
  struct hash_node* parent;
};


struct hash_node* createHash ( struct Treap* new_value, unsigned int size );


void printHash ( struct hash_node* );


/*
 * Retorna o hash com o novo valor inserido/atualizado
 */
struct hash_node* update ( struct hash_node* hash_root, struct Treap* new_value );

/*
 * Retorna o valor de hash(i,j)
 * O nó não é modificado
 */
struct Treap* retriveValue (struct hash_node* hash_root, unsigned int i, unsigned int j);

/*
 * Remove hash(i,j)
 */
void deleteHash(struct hash_node* hash_root, unsigned int i, unsigned int j );

#endif
