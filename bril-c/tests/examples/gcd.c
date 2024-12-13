#include <stdio.h>

// Compute the GCD of two positive integers using the Euclidean algorithm
int gcd(int op1, int op2) {
    for (; op1 != 0 && op2 != 0;) {
        if (op1 < op2) {
            op2 = op2 - op1;
        } else {
            op1 = op1 - op2;
        }
    }
    if(op1 == 0){
        return op2;
    } else {
        return op1;
    }
}

int main() {
    int op1 = 4;   // First input
    int op2 = 20;  // Second input

    int result = gcd(op1, op2); // Compute GCD
    printf("%d\n", result);    // Print the result

    return 0;
}
