#include <stdio.h>
#include <stdbool.h>

// Function to print primes in the interval [a, b]
void printPrimes(int a, int b) {
    // Start at max(a, 2) since primes are >= 2
    int start = a;
    if (a < 2) {
        start = 2;
    }

    for (int i = start; i <= b; ++i) {
        bool isPrime = true; // Assume `i` is prime

        // Check divisors from 2 to sqrt(i)
        for (int j = 2; j * j <= i; ++j) {
            if (i % j == 0) {
                isPrime = false;
                break; // Not a prime
            }
        }

        // If `i` is prime, print it
        if (isPrime) {
            printf("%d\n", i);
        }
    }
}

int main() {
    int a = 1;    // Start of the interval
    int b = 1000; // End of the interval

    printPrimes(a, b); // Print primes in the interval [a, b]
    return 0;
}
