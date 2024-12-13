#include <stdio.h>

// Function to compute the remainder (val % mod)
int getMod(int val, int mod) {
    return val - (val / mod) * mod;
}

// Function to compute the least common multiple (LCM)
void findLCM(int x, int y) {
    int greater = (x > y) ? x : y; // Start with the larger of the two numbers

    for (;; greater++) { // Infinite loop until LCM is found
        int modX = getMod(greater, x);
        int modY = getMod(greater, y);

        if (modX == 0 && modY == 0) { // Check if `greater` is divisible by both x and y
            printf("%d\n", greater);
            break;
        }
    }
}

int main() {
    int x = 64; // First input
    int y = 24; // Second input

    findLCM(x, y); // Compute and print LCM
    return 0;
}
