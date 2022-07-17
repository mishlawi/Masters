#include <stdio.h>
#include <stdlib.h>
#include "papi.h"

#define QTS_NUMEROS 20000000
#define QTS_BUCKETZ 10
#define INTERVAL (RAND_MAX/QTS_BUCKETZ)  
#define COLUNAS (QTS_NUMEROS/QTS_BUCKETZ)*2

#define NUM_EVENTS 4
int Events[NUM_EVENTS] = { PAPI_TOT_CYC, PAPI_TOT_INS,PAPI_L1_DCM,PAPI_L2_DCM};
// PAPI counters' values
long long values[NUM_EVENTS], min_values[NUM_EVENTS];

// number of times the function is executed and measured
#define NUM_RUNS 5


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


long long start_usec, end_usec, elapsed_usec, min_usec=0L;
     int m_size, total_elements, version, i, run;
     int num_hwcntrs = 0;
     fprintf (stdout, "\nSetting up PAPI...");
      // Initialize PAPI 
      PAPI_library_init (PAPI_VER_CURRENT);
      /* Get the number of hardware counters available */
      if ((num_hwcntrs = PAPI_num_counters()) <= PAPI_OK)  {
        fprintf (stderr, "PAPI error getting number of available hardware counters!\n");
        return 0;
      }
      fprintf(stdout, "done!\nThis system has %d available counters.\n\n", num_hwcntrs);

       // We will be using at most NUM_EVENTS counters
      if (num_hwcntrs >= NUM_EVENTS) {
        num_hwcntrs = NUM_EVENTS;
      } else {
        fprintf (stderr, "Error: there aren't enough counters to monitor %d events!\n", NUM_EVENTS);
        return 0;
    }

     // use PAPI timer (usecs) - note that this is wall clock time
       // for process time running in user mode -> PAPI_get_virt_usec()
       // real and virtual clock cycles can also be read using the equivalent
       // PAPI_get[real|virt]_cyc()
       start_usec = PAPI_get_real_usec();

    /* Start counting events */
   if (PAPI_start_counters(Events, num_hwcntrs) != PAPI_OK) {
     fprintf (stderr, "PAPI error starting counters!\n");
     return 0;
   }





    int aux,k,jaka,j;


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





   /* Stop counting events */
   if (PAPI_stop_counters(values, NUM_EVENTS) != PAPI_OK) {
     fprintf (stderr, "PAPI error stoping counters!\n");
     return 0;
   }

   end_usec = PAPI_get_real_usec();
   fprintf (stderr, "done!\n");

   elapsed_usec = end_usec - start_usec;

   if ((run==0) || (elapsed_usec < min_usec)) {
      min_usec = elapsed_usec;
      for (i=0 ; i< NUM_EVENTS ; i++) min_values[i] = values [i];
   }

  
   printf ("\nN= %d", QTS_NUMEROS);
   printf ("\nNumero de BUCKETS: %d\n", QTS_BUCKETZ);

   printf ("\nWall clock time aqui: %.4f secs\n", (min_usec/1000000.f));





  
  // output PAPI counters' values
  for (i=0 ; i< NUM_EVENTS ; i++) {
      char EventCodeStr[PAPI_MAX_STR_LEN];

      if (PAPI_event_code_to_name(Events[i], EventCodeStr) == PAPI_OK) {
        fprintf (stdout, "%s = %lld\n", EventCodeStr, min_values[i]);
      } else {
        fprintf (stdout, "PAPI UNKNOWN EVENT = %lld\n", min_values[i]);
      }
  }

#if NUM_EVENTS >1
  // evaluate CPI and Texec here
  if ((Events[0] == PAPI_TOT_CYC) && (Events[1] == PAPI_TOT_INS)) {
    float CPI = ((float) min_values[0]) / ((float) min_values[1]);
    fprintf (stdout, "CPI = %.2f\n", CPI);
  }
#endif












}

