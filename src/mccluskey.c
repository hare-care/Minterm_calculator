#include <stdio.h>

int main() {

    int num_minterms;
    printf("Enter number of minterms: ");
    scanf("%d", &num_minterms);

    int minterms[num_minterms];
    for (int i = 0; i < num_minterms; i++) {
        printf("Enter minterm: ");
        scanf("%d", minterms +i);
    };
    for (int i = 0; i < num_minterms; i++) {
        printf("%d\n", minterms[i]);
    };
    return 0;
}