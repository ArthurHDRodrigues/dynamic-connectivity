#include <stdio.h>
#include <stdlib.h>

#include "eulerSequence.h"
#include "dynamic_florest.h"

int main(){
  unsigned int n = 20;
  unsigned int m = n-1;

  struct dynamicForest amazonia = createDynamicForest(n);
  
  int i=0;
  srand(2);
  while (i<m) {
    unsigned int x = rand() % n;
    unsigned int y = rand() % n;
    
    struct Treap* raizA = find(&(amazonia.Forest[x]));
    struct Treap* raizB = find(&(amazonia.Forest[y]));
    
    if ( raizA != raizB ){
      i++;
      //link(&amazonia, raizA, raizB);
      concatenate(raizA, raizB);
    }
  }
  
  printf("\nÁRVORE:\n");
  printSeq(find(&(amazonia.Forest[0])));
  printf("\n");
  
  struct Treap* raiz = find(&(amazonia.Forest[0]));
  
  unsigned int o = 28;
  struct Treap* alvo_corte = search(raiz, o);
  struct Treap* ancora_L = search(raiz, o+1);
  //TODO: struct Treap* ancora_R = search(raiz, o-1);
  struct Treap* ancora_R = search(raiz, order(alvo_corte->inv)+1);
  printf("arco a cortar: ");
  printTreap(alvo_corte);
  printf("\n");
  
  cut(&(amazonia), alvo_corte);
  
  printf("\nsequência depois cut: \n");
  printSeq(find(ancora_L));
  printf("\n\n");
  printSeq(find(ancora_R));
  printf("\n");
  
  link(&(amazonia), &(amazonia.Forest[11]), &(amazonia.Forest[15]));
  
  printf("\nsequência depois link: \n");
  printSeq(find(&(amazonia.Forest[0])));
  printf("\n");
  
  exit(0);
};
