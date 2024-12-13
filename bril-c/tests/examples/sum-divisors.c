#include <stdio.h>

// Function to find the sum of all positive divisors of an integer `n`
void sum_of_divisors(int n) {
    int res = 0; // To store the sum of divisors

    // Handle negative input by taking the absolute value
    if (n < 0) {
        n = -n;
    }

    for (int i = 1; i * i <= n; ++i) {
        if (n % i == 0) { // Check if `i` is a divisor
            printf("%d\n", i); // Print the divisor
            res += i;

            int d = n / i; // Find the corresponding divisor `n / i`
            if (d != i) { // Avoid double counting if `i` is the square root of `n`
                printf("%d\n", d);
                res += d;
            }
        }
    }

    // Print the sum of divisors
    printf("%d\n", res);
}

int main() {
    int n = 100; // Input value
    sum_of_divisors(n); // Calculate and print divisors and their sum
    return 0;
}
