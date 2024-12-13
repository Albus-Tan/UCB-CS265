#include <stdio.h>
#include <stdbool.h>

// Extract the last digit of a number
int last_digit(int x) {
    return x % 10;
}

// Check if the digits of a number are in strictly decreasing order
bool is_decreasing(int x) {
    int prev = -1; // Initialize to a value less than any digit

    for (; x > 0;) {
        int digit = last_digit(x);

        if (digit <= prev) {
            return false; // Not strictly decreasing
        }

        prev = digit; // Update previous digit
        x /= 10;      // Remove the last digit
    }

    return true; // All digits are strictly decreasing
}

int main() {
    int x = 954320; // Input number

    bool result = is_decreasing(x); // Check if digits are strictly decreasing
    printf("%d\n", result);         // Print the result (1 for true, 0 for false)

    return 0;
}
