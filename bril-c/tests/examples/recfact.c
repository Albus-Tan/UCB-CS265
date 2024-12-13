#include <stdio.h>

// Recursive function to compute the factorial of a number
int fac(int x) {
    if (x <= 1) {
        return 1; // Base case: factorial of 1 or 0 is 1
    } else {
        return x * fac(x - 1); // Recursive case
    }
}

int main() {
    int input = 8; // Input value
    int result = fac(input); // Compute the factorial
    printf("%d\n", result);  // Print the result
    return 0;
}
