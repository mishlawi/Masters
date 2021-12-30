#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

/*
In order to use OpenMP’s directives, we will have to include the header file: "omp.h".
Whilst compilation, we’ll have to include the flag -fopenmp.
All the directives start with #pragma omp
*/


/*
Example made by me:
Given a size 10 array: 
14 ; 24 ; 12 ; 65 ; 15 ; 75 ; 34 ; 87 ; 35 ; 81;

14 12 15 -> bucket 1
24 -> bucket 2
34 35 -> bucket 3
65 -> bucket 6
75 -> bucket 7
87 81 -> bucket 8

sort each bucket so that
bucket 1 == 12 14 15
bucket 2 == 24
bucket 3 == 34 35
bucket 6 == 65
bucket 7 == 75
bucket 8 == 81 87

final array:
12 ; 14 ; 15 ; 24 ; 34 ; 35 ; 65 ; 75 ; 81 ; 87;
*/



# define CAP 10

int B; // * buckets
int min; // * min value of the input array
int max; // * max value of the input array

/* 
 maybe get a user defined array
* or generate it in a random way <----
! we need to define the bucket vector:
   * an array of BUCKETS each having its own bucket list
   ? maybe an array of buckets instead of a list ?
*/  


// Bucket 


struct Bucket
{
    int value;
    struct Bucket *prox;
};

/**
 * @brief Get a random number in a specific interval
 * 
 * @param low 
 * @param up 
 * @param N 
 * @return int 
 */
int getRand(int low, int up, int N)
{ 

    int nrGen = (rand() % (up - low + 1)) + low;
    return nrGen;
}



/**
 * @brief Get the array with random values
 * 
 * @param low 
 * @param up 
 * @param number 
 * @return int* 
 */
int * getRandArray(int low, int up, int number){
   // char *str_to_ret = malloc(sizeof(char) * required_size);
    int *r = malloc(sizeof(int)*number);
    int i;


    srand((unsigned)time(NULL));
    r[0] = getRand(low,up,number);
    min = r[0];
    max = min;
    printf("r[0] = %d\n", r[0]);
    for (i = 1; i < number; ++i)
    {
        
        r[i] = getRand(low,up,number);
        if(min > r[i]) {
            min = r[i];
        }
        if(max < r[i]) {
            max = r[i];
        }
        printf("r[%d] = %d\n", i, r[i]);
    }
    //free(r);
    printf("%d\n", min);
    printf("%d\n", max);
    // ! dont forget to understand all the concepts of malloc and free
    // TODO ->  Add free(r) de forma conveniente
    
    return r;
}

struct Bucket ** initBuckets(int size)
{
    struct Bucket **buckets;
    buckets = (struct Bucket **)malloc(sizeof(struct Bucket *) * size);
    for(int i=0;i<size;i++){
        buckets[i]=NULL;
    }
    
return buckets;
}

void printBuckets(struct Bucket **buckets,int size){
    printf("*******************\n");
    for (int i=0;i<size;i++){
        printf("No bucket %d há:\n", i );
        if(buckets[i]!=NULL){
            printf(".%d\n",buckets[i]->value);
            struct Bucket *atm = buckets[i];
            while(atm->prox!=NULL){
                printf(".%d\n",atm->prox->value);
                atm=atm->prox;
            }
        }
        
       
    }

}

int main(int argc, char *argv[])
{

    if (argc != 5)
    {
        printf("*Lacking or overgiving arguments\n\n./main [valor inferior] [valor superior] [nr elementos array] [nr de buckets] \n");
        return 1;
    }
    int low = atoi(argv[1]);
    int up = atoi(argv[2]);
    int N = atoi(argv[3]);
    B = atoi(argv[4]);
    int *arr;

    arr = getRandArray(low, up, N); // generates the array with random elements
   
    int range;
    range = (max - min) / B+1;

    printf("Range de cada bucket: %d\n", range); // TODO: eliminar estes comentarios
    
 
    int index;
     // * array of buckets
    struct Bucket **buckets = initBuckets(B);
        // ! where the sorting of the values to different buckets happens
        for (int i = 0; i < N; i++)
        {
            struct Bucket *new = (struct Bucket *)malloc(sizeof(struct Bucket *));
            index = (arr[i] - min) / range;          
            if (buckets[index] == NULL)
            {
                printf("O %d entrou no Bucket nr:%d\n", arr[i], index);
                new->value = arr[i];
                new->prox= NULL;
                buckets[index]= new;                
            }   
            else
            {
                printf("O %d entrou no Bucket com elementos nr:%d\n", arr[i], index);
                struct Bucket *atm = buckets[index];
                
                while (atm->prox != NULL)  atm = atm->prox;
                
                atm->prox = (struct Bucket *)malloc(sizeof(struct Bucket *));
                atm->prox->value = arr[i];
                atm->prox->prox = NULL;
            }
        }
        printBuckets(buckets,B);
         return 0;
    }
