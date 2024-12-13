#include <stdio.h>

// Function to compute the sum of squares from 1 to n
int sumOfSquares(int n) {
    int res = 0;
    for (int i = 1; i <= n; ++i) {
        res += i * i; // Add square of i to result
    }
    return res;
}

// Function to compute the square of the sum from 1 to n
int squareOfSum(int n) {
    int res = 0;
    for (int i = 1; i <= n; ++i) {
        res += i; // Add i to the sum
    }
    return res * res; // Square the sum
}

int main() {
    int n = 100; // Input value

    // Compute the sum of squares and the square of the sum
    int sum = sumOfSquares(n);
    int square = squareOfSum(n);

    // Compute the difference
    int diff = square - sum;

    // Print the result
    printf("%d\n", diff);

    return 0;
}
