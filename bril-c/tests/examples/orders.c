#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

// Compute the absolute value of a number
int abs_val(int a) {
    if (a < 0) {
        return -a;
    } else {
        return a;
    }
}

// Compute gcd using Euclid's algorithm
int gcd(int a, int b) {
    for ( ; b != 0; ) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

// Compute lcm using lcm(a, b) = |a * b| / gcd(a, b)
int lcm(int a, int b) {
    if (a == 0 || b == 0) return 0;
    return abs_val(a * b) / gcd(a, b);
}

// Compute the orders of elements [1, n)
void orders(int n, bool use_lcm) {
    for (int u = 1; u < n; ++u) {
        int order = 0;
        if (use_lcm) {
            order = lcm(u, n) / u; // Compute using lcm
        } else {
            order = n / gcd(u, n); // Compute using gcd
        }
        printf("%d\n", u);
        printf("%d\n", order);
    }
}

int main() {
    int n = 96;      // Modulo value
    bool use_lcm = false; // Whether to use lcm to compute orders

    // Print order of 0
    printf("%d\n", 0);
    printf("%d\n", 1);

    // Compute orders for [1, n)
    orders(abs_val(n), use_lcm);

    return 0;
}
