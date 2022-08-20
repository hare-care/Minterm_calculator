#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct {
    unsigned int num_true;
    bool checked;
    unsigned* array_ptr;
} minterm_t;

unsigned* bin(unsigned n, size_t length)
{
    int num_true = 0;
    unsigned* array = malloc(length * sizeof(unsigned));
    int count = 0;
    unsigned i;
    for (i = 1 << (length - 1); i > 0; i = i / 2) {
        if (n & i) {
            array[count] = 1;
            num_true++;
        } else {
            array[count] = 0;
        };
        count++;
    }
    return array;
}

void initialize_minterm(int n) {
    

}

/* Used to print array contents for testing */
void print_array(unsigned* array_ptr, size_t length) {
    for (int i = 0; i < length; i++) {
        printf("Index %d: %d\n", i, array_ptr[i]);
    }
}


int main(int argc, char* argv[]) {
    /*
    * args to main are going to be length of minterms (argc -1)
    * as well as argv which holds the minterms from index 1 to n
    * Will go through argv to convert from char to int and place into new array
    */
   int num_minterms = argc - 1;
   int minterms[num_minterms];
   for (int i = 1; i < argc; i++) {
       minterms[i - 1] = atoi(argv[i]);
   };

   for (int i = 0; i < num_minterms; i++){
       printf("Minterm #%d: %d\n", i, minterms[i]);
   };
   unsigned* test_array = bin(0, 4);
   print_array(test_array, 4);
   free(test_array);
   
   



   
    return 0;
}