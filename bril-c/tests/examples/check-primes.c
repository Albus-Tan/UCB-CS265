#include <stdio.h>
#include <stdbool.h>

// Check if a number is prime
int checkPrime(int x) {
    if (x <= 1) {
        return 0;
    }
    for (int i = 2; i < x; i++) {
        if (x % i == 0) {
            return 0;
        }
    }
    return 1;
}

// Main function
int main() {
    int n = 50;

    for (int i = 1; i < n; ++i) {
        printf("%d\n", checkPrime(i)); // Print 1 if the number is prime
    }

    return 0;
}
