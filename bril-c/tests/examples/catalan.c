#include <stdio.h>

// Compute the nth term in the catalan sequence
int catalan(int n) {
    if (n == 0) {
        return 1;
    }

    int sum = 0;
    n -= 1; // Compute for c(n+1) based on 0-based indexing

    for (int idx = 0; idx <= n; ++idx) {
        int n2 = n - idx;
        int v1 = catalan(idx);
        int v2 = catalan(n2);
        sum += v1 * v2;
    }

    return sum;
}

int main() {
    int input = 10;

    int catn = catalan(input);
    printf("%d\n", catn);

    return 0;
}
