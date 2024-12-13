#include <stdio.h>
#include <stdbool.h>

// Function to compute the sum of [1, n] using a loop
int sum_by_loop(int n) {
    int sum = 0;
    for (int i = 1; i <= n; ++i) {
        sum += i;
    }
    return sum;
}

// Function to compute the sum of [1, n] using the formula
int sum_by_formula(int n) {
    return (1 + n) * n / 2;
}

int main() {
    int n = 1000; // Input value

    // Compute the sum using both methods
    int first = sum_by_loop(n);
    int second = sum_by_formula(n);

    // Compare the results
    bool isSame = (first == second);

    // Print the results
    printf("%d\n", first);  // Sum by loop
    printf("%d\n", second); // Sum by formula
    printf("%d\n", isSame); // 1 if the results are the same, 0 otherwise

    return 0;
}
