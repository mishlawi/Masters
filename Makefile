CC=gcc
CFLAGS= -g -O2
DEPS =
OBJ = main.o
LIB = -fopenmp

%.o: %.c $(DEPS)
	$(CC) $(CFLAGS) -c -o $@ $< $(LIB)

parallelBucketSort: $(OBJ)
	gcc $(CFLAGS) -o $@ $^ $(LIB)

clean:
	rm *.o parallelBucketSort
