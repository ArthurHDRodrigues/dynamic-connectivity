#include <stdlib.h>
#include "eulerSequence.h"
#include "dynamic_florest.h"

/**************************************************\
 *                  Dynamic Tree                  *
\**************************************************/

struct dynamicForest createDynamicForest(unsigned int n){
  /*
   * Devolve uma árvore dinámica com n vértices
   */
  struct dynamicForest retorno = {
    .n = n,
    .Forest = malloc(n*sizeof(struct Treap)),
  };
  
  struct vertice v;
  for(int i=0; i<n; i++){
    v.id = i;
    retorno.Forest[i] = eulerSeq( v, v);
  }
  return retorno;
}

int fconnected(struct dynamicForest* F, struct Treap* v, struct Treap* w){
  /*
   * Testa se v e w estão na mesma componente conexa de F
   */
  return find(v) == find(w);
}


void link (struct dynamicForest* F, struct Treap* v, struct Treap* w){
  /*
   * Recebe a floresta e dois vértices dela e os conecta com uma aresta
   */
  bringToFront(v);
  bringToFront(w);

  struct Treap* VW = malloc(sizeof(struct Treap));
  struct Treap* WV = malloc(sizeof(struct Treap));
  struct Treap* VV = malloc(sizeof(struct Treap));
  
  struct Treap* ww = search(w,1); //TODO ver se não devia ser raiz!
  struct Treap* vv = search(v,1);
  
  *VW = eulerSeq(vv->valor.to, ww->valor.to);
  *WV = eulerSeq(ww->valor.to, vv->valor.to);
  *VV = eulerSeq(vv->valor.to, vv->valor.to);
  
  join(join(join(join(v, VW), w), WV), VV);
}


void cut (struct dynamicForest* F, struct Treap* vw){
   /*
    * Recebe uma floresta e uma aresta dela e a remove
    */
   
   //Verifica se a treap é de fato um arco e não um nó da forma VV
   if( vw->valor.to.id != vw->valor.from.id ) {
     // Garante que vw ocorra antes de wv na sequência
     if ( order(vw) > order(vw->inv)) return cut(F,vw->inv);
     
     struct Treap* raiz = find(vw);
     unsigned int K  = order(vw);
   
     struct Treap* R = slice(&raiz, K-2);
     
     // Inicio de R = (vv vw ww ...)
     // TODO: Pensar nos free()
     // TODO: Garantir que os nós vv que estão no vetor não estejam R[1..2]
     R = slice(&R, 2);
     
     unsigned int Q = order(vw->inv); //Pode ou não estar na mesma sequência de vw
     struct Treap* L = slice(&R, Q-1); // R fica correto!
     L = slice(&L, 1); // remove o inverso
          
     join(raiz, L);
  }
}

