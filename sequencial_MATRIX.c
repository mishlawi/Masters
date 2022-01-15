#include <stdio.h>
#include <stdlib.h>


#define QTS_NUMEROS 20000000
#define QTS_BUCKETZ 10  
#define INTERVAL (RAND_MAX/QTS_BUCKETZ)  
#define COLUNAS (QTS_NUMEROS/QTS_BUCKETZ)*2


void quicksort(int number[],int first,int last){
    int ikk, jkk, pivot, temp;

    if(first<last){
        pivot=first;
        ikk=first;
        jkk=last;

        while(ikk<jkk){
            while(number[ikk]<=number[pivot]&&ikk<last)
                ikk++;
            while(number[jkk]>number[pivot])
                jkk--;
            if(ikk<jkk){
                temp=number[ikk];
                number[ikk]=number[jkk];
                number[jkk]=temp;
            }
        }

        temp=number[pivot];
        number[pivot]=number[jkk];
        number[jkk]=temp;
        
        quicksort(number,first,jkk-1);
        quicksort(number,jkk+1,last);
    }
}


int main(int argc, char *argv[]){
    int i,aux,k,jaka,j;

    srand(1995);

    int array_de_preenchidos[QTS_BUCKETZ];


    int (*matriz)[COLUNAS];
    matriz=(int (*)[COLUNAS])malloc(sizeof(*matriz)*QTS_BUCKETZ);


    for (i = 0; i < QTS_BUCKETZ; i++) //meter cada gajo do array  preenchidos a 0
        array_de_preenchidos[i] = 0;

   for (i = 0; i < QTS_NUMEROS; i++){ 
        aux=rand();
        k=0;
        jaka=INTERVAL;
        while(jaka<aux){
            k++;
            jaka=jaka+INTERVAL;
        }

        matriz[k][array_de_preenchidos[k]]=aux;
        array_de_preenchidos[k]++;
    }



    //PRINT MATRIXXXXXX
    /*


    for (i = 0; i < QTS_BUCKETZ; i++){ 
        printf("\nArray %d: ",i);
        for (j = 0; j < array_de_preenchidos[i]; j++){ 
            printf(" %d ",matriz[i][j]);
            }

    }
    */

    //QUICKSORT A TODOS OS BUCKETS

    for (i = 0; i < QTS_BUCKETZ; i++)
        quicksort(matriz[i],0,array_de_preenchidos[i]-1);
    



       ///////////////COMEÇAR A PREENCHER O ARRAY/////////////////////

    int* vector_final = (int*) malloc(sizeof(int) * QTS_NUMEROS);
    k=0;
    for (i = 0; i < QTS_BUCKETZ; i++){
        for (j = 0; j < array_de_preenchidos[i]; j++){ 
            vector_final[k]=matriz[i][j];
            k++;
        }

    }

    //imprimir o vector final
    /*
    for (i = 0; i < QTS_NUMEROS; i++){ 
        printf("| %d |",vector_final[i]);


    }
    printf("\n\n");
    */

    
    //passar para texto so para verificar os paralelos
    /*
    FILE *fp;
    if((fp=fopen("array.txt", "w"))==NULL) {
    printf("Cannot open file.\n");
    }

    if(fwrite( vector_final, sizeof(int), 137550, fp ) !=137550)
          printf("File read error.");
     fclose(fp);
    */



    // LER O ARRAY.TXT
    /*
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
    */









}

