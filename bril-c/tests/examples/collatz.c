#include <stdio.h>

// Compute the Collatz sequence starting from x
void collatz(int x) {
    for (; x != 1; ) { // Loop until x becomes 1
        printf("%d\n", x); // Print the current value

        if (x % 2 == 0) {
            x = x / 2; // If x is even
        } else {
            x = x * 3 + 1; // If x is odd
        }
    }
    printf("%d\n", x); // Print the final value (1)
}

int main() {
    int x = 7; // Input argument
    collatz(x);
    return 0;
}
