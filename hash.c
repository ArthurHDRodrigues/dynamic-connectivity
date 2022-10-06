#include <stdio.h>
#include <stdlib.h>
#include "hash.h"
#include <assert.h>
  
struct hash_node* createHash ( struct Treap* new_value, unsigned int size) {
  // Se a hash_root estiver vazia, então cria uma nova
  assert ( new_value );
  unsigned int i = new_value->valor.from.id;
  unsigned int j = new_value->valor.to.id;
  
  double fraction = ((i*size+j)*GOLDEN_RATIO);
  
  // remove a parte inteira
  fraction = fraction - ((long)fraction);
  printf("frac: %f\n", fraction);
  
  struct hash_node dummy = {
    .valor = new_value,
    .size = size,
    .prio = rand(),
    .index= (unsigned int)(4*size*fraction),
    .esq = NULL,
    .dir = NULL,
    .parent = NULL,
  };
  
  
  struct hash_node* retorno = malloc(sizeof(struct hash_node));
  if ( !retorno ){
    printf("Erro ao alocar memória para novo nó de hash\n");
    exit(1);
  };
  
  *retorno = dummy;
  
  return retorno;
}



void printHash(struct hash_node* hash){
    if ( hash ){
      if ( hash->esq ) printHash(hash->esq);
      printf("index: %u\n", hash->index);
      printTreap(hash->valor);
      if ( hash->dir ) printHash(hash->dir);
    } else printf("NULL");
}
  
struct hash_node* searchHashRec( struct hash_node* hash_root, unsigned int index){
  if ( hash_root ) {
    if ( hash_root->index < index ) return searchHashRec( hash_root->dir, index);
    if ( hash_root->index > index ) return searchHashRec( hash_root->esq, index);
    return hash_root;
  } return NULL;
}

struct hash_node* searchHash( struct hash_node* hash_root, unsigned int i, unsigned int j){
  unsigned int size = hash_root->size;
  double fraction = ((i*size+j)*GOLDEN_RATIO);
  fraction = fraction - ((long)fraction);
  unsigned int index= (unsigned int)(4*size*fraction);
  
  return searchHashRec( hash_root, index);
}

struct hash_node* update ( struct hash_node* hash_root, struct Treap* new_value ){
  assert ( hash_root );
  assert ( new_value );
  struct hash_node* old_hash = searchHash(hash_root, new_value->valor.from.id,  new_value->valor.to.id);
  
}

//struct eulerSeqElem retriveValue (struct hash_node* hash_root, unsigned int i, unsigned int j);

//void remove(struct hash_node* hash_root, unsigned int i, unsigned int j );
