#include <stdio.h>

// Main function logic
void calculate(int n, int p) {
    int two = 2;
    int m = p - two; // m = p - 2
    int ans = 1;
    int a = n;

    // Loop to calculate the result
    for (; m > 0; m /= two) {
        if (m != (m / two) * two) { // If m is odd
            ans = (ans * a) % p;
        }
        a = (a * a) % p; // Square a and take mod p
    }

    // Print the final result
    printf("%d\n", ans);
}

int main() {
    int n = 46;      // Input number
    int p = 10007;   // Modulo value

    calculate(n, p); // Perform calculation
    return 0;
}
