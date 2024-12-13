#include <stdio.h>

// Function to check if n is the hypotenuse of a Pythagorean triple
void findPythagoreanTriples(int n) {
    int n_sq = n * n; // Square of n

    for (int a = 1; a < n; ++a) { // Iterate through potential values of a
        for (int b = 1; b <= a; ++b) { // Iterate through potential values of b
            int a_sq = a * a;
            int b_sq = b * b;
            int sum = a_sq + b_sq;

            if (sum == n_sq) { // Check if a^2 + b^2 = n^2
                printf("%d\n", b); // Print the pair (b, a)
                printf("%d\n", a);
            }
        }
    }
}

int main() {
    int n = 125; // Input value
    findPythagoreanTriples(n); // Find and print Pythagorean triples
    return 0;
}
