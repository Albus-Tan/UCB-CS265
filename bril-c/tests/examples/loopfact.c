#include <stdio.h>

// Function to compute the factorial of a number
int factorial(int input) {
    int result = 1; // Initialize result to 1

    for (int i = input; i > 0; --i) {
        result *= i; // Multiply result by the current value of i
    }

    return result;
}

int main() {
    int input = 8; // Input value

    int result = factorial(input); // Compute factorial
    printf("%d\n", result);        // Print the result

    return 0;
}
