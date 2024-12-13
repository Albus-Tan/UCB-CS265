#include <stdio.h>
#include <stdbool.h>

// Function to determine if a number is odd (returns true if residue is 1)
bool mod2(int a) {
    return (a % 2) == 1;
}

// Subroutine to perform bitwise operation (AND or OR) on two numbers
int loop_subroutine(int a, int b, bool is_or) {
    int ans = 0;
    int to_add = 1;
    for (int i = 0; i <= 63; ++i) {
        bool mod2a = mod2(a);
        bool mod2b = mod2(b);
        if(is_or) {
            if (mod2a || mod2b) {
                ans += to_add;
            }
        } else {
            if (mod2a && mod2b) {
                ans += to_add;
            }
        }

        a /= 2;
        b /= 2;
        to_add *= 2;
    }
    return ans;
}

// Bitwise OR operation
int OR(int a, int b) {
    return loop_subroutine(a, b, true);
}

// Bitwise AND operation
int AND(int a, int b) {
    return loop_subroutine(a, b, false);
}

// Bitwise XOR operation
int XOR(int a, int b) {
    return OR(a, b) - AND(a, b);
}

int main() {
    int a = 7;   // First input
    int b = 15;  // Second input
    int c = 0;   // Operation selection: 0 for AND, 1 for OR, 2+ for XOR

    int ans = 0;
    if (c - 1 < 0) { // AND
        ans = AND(a, b);
    } else if (c - 1 == 0) { // OR
        ans = OR(a, b);
    } else { // XOR
        ans = XOR(a, b);
    }

    printf("%d\n", ans); // Print the result
    return 0;
}
