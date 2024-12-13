#include <stdio.h>

// Function to generate the nth row of Pascal's Triangle
void generateNthRow(int x) {
    int prev = 1;
    printf("%d\n", prev); // Print the first element (always 1)

    for (int i = 0; i < x; ++i) {
        int temp = x - i;       // Compute (x - i)
        int curr = prev * (temp + 1); // Compute current value: prev * (x - i + 1)
        printf("%d\n", curr);   // Print the current value
        prev = curr;            // Update prev to the current value
    }
}

int main() {
    int x = 5; // Input value for the nth row
    generateNthRow(x); // Generate and print the nth row
    return 0;
}
