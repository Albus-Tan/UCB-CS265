#include <stdio.h>

// Function to compute dividend % divisor
int mod(int dividend, int divisor) {
    int quotient = dividend / divisor;
    return dividend - (quotient * divisor);
}

// Function to compute the number of 1s in the binary representation of an integer
void countBinaryOnes(int input) {
    int sum = 0;
    int two = 2;

    for (; input != 0;) {
        int bit = mod(input, two); // Get the last binary digit
        input = input / two;      // Shift the binary number to the right
        sum += bit;               // Add the bit to the sum
    }

    printf("%d\n", sum); // Print the total number of 1s
}

int main() {
    int input = 42; // Input value
    countBinaryOnes(input); // Count and print the number of 1s
    return 0;
}
