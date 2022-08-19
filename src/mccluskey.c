#include <stdio.h>
#include <stdlib.h>

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
    return 0;
}