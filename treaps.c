/*
 * Implementação de uma Floresta Dinamica
 * Para compilar: gcc -Wall treaps.c -o treaps
 */

#include <stdio.h>
#include <stdlib.h>

/**************************************************\
 *         Estrutura básica para grafos           *
\**************************************************/
struct vertice{
  unsigned int id;
};

// Declaração de elemento de sequência
struct eulerSeqElem{
  struct vertice from;
  struct vertice to;
};

void printSeqElem(struct eulerSeqElem* A){
  if ( A ) printf("%u %u,", A->from.id,A->to.id);
  else printf("NULL");
}

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

/**************************************************\
 *                  Dynamic Tree                  *
\**************************************************/

struct dynamicForest{
  // Número de vértices da árvore
  unsigned int n;
  // Vetor de árvores de tamanho n alocado dinamicamente
  struct Treap* Forest;
};

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
      concatenate(raizA, raizB);
    }
  }
  
  printf("\nÁRVORE:\n");
  printSeq(find(&(amazonia.Forest[0])));
  
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
