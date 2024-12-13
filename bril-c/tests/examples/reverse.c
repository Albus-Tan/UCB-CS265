#include <stdio.h>
#include <stdbool.h>

// Function to reverse the digits of an integer
int reverseDigits(int n) {
    int result = 0;
    int base = 10; // Base for decimal numbers

    for (bool notdone = true; notdone;) {
        int remainder = n % base; // Extract the last digit
        result = result * base + remainder; // Add it to the reversed result
        n /= base; // Remove the last digit from n

        if (n == 0) {
            notdone = false; // Stop when no digits are left
        }
    }

    return result;
}

int main() {
    int input = 123; // Input value
    int result = reverseDigits(input); // Reverse the digits
    printf("%d\n", result); // Print the result
    return 0;
}
