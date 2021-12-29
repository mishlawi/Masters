/**
 * @file main.c
 * @author mishlawi
 * @brief 
 * @version 0.1
 * @date 2021-12-10
 * 
 * @copyright Copyright (c) 2021
 * 
 */

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

#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

# define BUCKETS 5
# define CAP 10
/* 
maybe get a user defined array
or generate it in a random way <----
we need to define de bucket vector:
we need a bucket vector
*/
struct bucket
{
    int value;
    struct bucket;

};


int getRand(int low, int up, int N)
{ 

    int nrGen = (rand() % (up - low + 1)) + low;
    return nrGen;
}

int * getRandArray(int low, int up, int number){

    int r[number];
    int i;
    srand((unsigned)time(NULL));

    for (i = 0; i < number; ++i)
    {
        
        r[i] = getRand(low,up,number);
        printf("r[%d] = %d\n", i, r[i]);
    }
    
    return r;
}





int main(int argc,char *argv[]){
    
    if( argc>4 || argc==1){
        printf("*Lacking arguments\n\n./main [inf. range of values] [sup. range of values] [Nr of elements in the array] \n");
        return 1;
    }
    
    int low = atoi(argv[1]);
    int up = atoi(argv[2]);
    int N = atoi(argv[3]);
    int *arr;

    arr = getRandArray(low,up,N);
    
    return 0;
} 
