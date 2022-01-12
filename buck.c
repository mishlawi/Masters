#include <stdio.h>
#include <stdlib.h>
#include<omp.h>

#define QTS_NUMEROS 200000
#define QTS_BUCKETZ 10  
#define INTERVAL (RAND_MAX/QTS_BUCKETZ)  


typedef struct elem {
  int x;
  struct elem *prox;
}ELLLLLL;

struct elem* adiciona_a_lista_no_sitio(int x1,struct elem* lista){
    struct elem* novo = malloc(sizeof(struct elem));
    struct elem* ant;
    struct elem* rett;
    novo->x=x1;

    if(lista){
        rett=lista;
        if(lista->x>x1){
            rett=novo;
            novo->prox=lista;
        }else{
        
            while(lista && lista->x<=x1){
                ant=lista;
                lista=lista->prox;
            }
            if(lista){
                novo->prox=ant->prox;
                ant->prox=novo;
            }
            else{
                novo->prox=NULL;
                ant->prox=novo;
            }
        }
    }
    else{
        novo->prox=NULL;
        rett= novo;
    }

    return rett;
}

void imprime_lista(struct elem* lista){
    while(lista){
        printf("%d -> ",lista->x);
        lista=lista->prox;
    }
    printf("NULL\n");
}

int conta_lista(struct elem* lista){
    int conta=0;
    while(lista){
        conta++;
        lista=lista->prox;
    }
    return conta;
}



int main(int argc, char *argv[]){
    int i,aux,k,jaka;

    srand(1995);

    struct elem* array_buckets[QTS_BUCKETZ];
   

    for (i = 0; i < QTS_BUCKETZ; i++) //meter cada lligada do array a NULL
        array_buckets[i] = NULL;

    #pragma omp parallel for 
    for (i = 0; i < QTS_NUMEROS; i++){ 
        //printf("A processar %d\n",i);
        aux=rand();
        k=0;
        jaka=INTERVAL;
        while(jaka<aux){
            k++;
            jaka=jaka+INTERVAL;
        }
        array_buckets[k]=adiciona_a_lista_no_sitio(aux,array_buckets[k]);//insere x elementos 
    }



    ///////////////COMEÇAR A PREENCHER O ARRAY/////////////////////


    printf("| a passar para o array |\n");

    int vector_final[QTS_NUMEROS];
    k=0;
    for (i = 0; i < QTS_BUCKETZ; i++){
        struct elem* lista = array_buckets[i];

        while(lista){
            vector_final[k]=lista->x;
            k++;
            lista=lista->prox;
        }

    }


    FILE *fp;
    int vector_check[137550];

    if((fp=fopen("array.txt", "rb"))==NULL) {
     printf("Cannot open file.\n");
    }

  if(fread(vector_check, sizeof(int), 137550, fp) != 137550) {
        if(feof(fp))
            printf("Premature end of file.");
        else
            printf("File read error.");
    }
  fclose(fp);

  for(i=0; i<137550; i++)
    if(vector_final[i]!=vector_check[i])
        printf("encontrado um numero errado");


    
    printf("\n\n| chegou ao fim plim |\n");






}

