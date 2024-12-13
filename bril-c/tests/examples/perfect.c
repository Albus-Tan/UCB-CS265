#include <stdio.h>
#include <stdbool.h>

// Main function to determine if a number is a perfect number
void checkPerfectNumber(int input) {
    int n = input;
    int sum = 1;      // Start with 1 since 1 is a divisor for all numbers
    int result = 1;   // Assume it's a perfect number unless proven otherwise

    for (int i = 2; i * i <= n; ++i) { // Loop until i^2 > n
        int quotient = n / i;
        int product = quotient * i;
        int remainder = n - product;

        if (remainder == 0) { // If n is divisible by i
            sum += i;
            if (i != quotient) { // Avoid adding the square root twice
                sum += quotient;
            }
        }
    }

    // Check if the sum of divisors equals the original number
    if (sum == n) {
        result = 0; // Mark as perfect number
    }

    // Print the result (0 if perfect, 1 otherwise)
    printf("%d\n", result);
}

int main() {
    int input = 496; // Input number
    checkPerfectNumber(input);
    return 0;
}
