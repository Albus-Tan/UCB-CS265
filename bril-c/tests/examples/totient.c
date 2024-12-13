#include <stdio.h>

// Function to compute Euler's Totient Function for a given n
int totient(int n) {
    int result = n; // Start with n
    int p = 2;      // Start checking from the smallest prime

    // Iterate over all possible factors up to sqrt(n)
    for (; p * p <= n; ++p) {
        // Check if p is a divisor of n
        if (n % p == 0) {
            // Divide n by p until it's no longer divisible
            for (; n % p == 0;) {
                n /= p;
            }
            // Update result using the formula result *= (1 - 1/p)
            result -= result / p;
        }
    }

    // If n is still greater than 1, it means n itself is prime
    if (n > 1) {
        result -= result / n;
    }

    return result;
}

int main() {
    int n = 2023; // Input value
    printf("%d\n", n); // Print the input value
    int tot = totient(n); // Compute Euler's Totient Function
    printf("%d\n", tot); // Print the result
    return 0;
}
