#include <stdio.h>

// Compute gcd using the Euclidean algorithm
int gcd(int a, int b) {
    // Ensure a >= b
    if (b > a) {
        int temp = a;
        a = b;
        b = temp;
    }

    for (; b != 0;) {
        int remainder = a % b;
        a = b;
        b = remainder;
    }

    return a;
}

// Print all integers less than or equal to `a` that are relatively prime to `a`
void relative_primes(int a) {
    for (int b = a; b >= 1; --b) {
        if (gcd(a, b) == 1) {
            printf("%d\n", b);
        }
    }
}

int main() {
    int a = 20; // Input value
    relative_primes(a); // Print all relative primes
    return 0;
}
