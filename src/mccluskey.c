#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct {
    unsigned int num_true;
    bool checked;
    unsigned* array_ptr;
    bool dont_care;
} minterm_t;

/* function to create a minterm from an int*/
minterm_t create_minterm(int n, size_t num_signals, bool dc_flag) {
    /* 
    * init vars
    * creates memory but does not free. 
    * Once the minterm is no longer needed, 
    * array_ptr of minterm must be freed
    */
    int num_true = 0;
    unsigned* array = malloc(num_signals * sizeof(unsigned));
    int count = 0;
    unsigned i;

    /*
    * shifting i to largest digit. compare if they match.
    * if yes, that bit is a 1, if no, that bit is a 0
    * then store that in the current index of array.
    * Every time its a one, add to num_true to keep track
    * Once array is full, create minterm object. 
    * minterms always start unchecked.
    */
    for (i = 1 << (num_signals - 1); i > 0; i = i / 2) {
        if (n & i) {
            array[count] = 1;
            num_true++;
        } else {
            array[count] = 0;
        };
        count++;
    }
    minterm_t minterm = {.array_ptr = array, 
                         .checked=false,
                         .num_true=num_true,
                         .dont_care=dc_flag};
    return minterm;
}

/* Used to print array contents for testing */
void print_array(unsigned* array_ptr, size_t length) {
    for (int i = 0; i < length; i++) {
        printf("%d,", array_ptr[i]);
    }
    printf("\n");
}


int main(int argc, char* argv[]) {
    /*
    * args to main are going to be length of minterms (argc -1)
    * as well as argv which holds the minterms from index 1 to n
    * Will go through argv to convert from char to int and place into new array
    */
   int num_minterms = argc - 1;
   minterm_t minterms[num_minterms];
   for (int i = 1; i < argc; i++) {
       int number = atoi(argv[i]);
       minterms[i - 1] = create_minterm(number, 4, false);
   };

   for (int i = 0; i < num_minterms; i++){
       printf("Minterm #%d: ", i);
       print_array(minterms[i].array_ptr, 4);
   };
   
   

    return 0;
}