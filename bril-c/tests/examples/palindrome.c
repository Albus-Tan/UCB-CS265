#include <stdio.h>
#include <stdbool.h>

// Compute base^exp using iteration
int cal_pow(int base, int exp) {
    int res = 1;
    for (; exp > 0; --exp) {
        res *= base;
    }
    return res;
}

// Check if a number is a palindrome
bool palindrome(int in, int len) {
    if (len <= 0) {
        return true; // Single digit or no digits left, it's a palindrome
    }

    int cal_power = cal_pow(10, len);      // Compute 10^len
    int left = in / cal_power;        // Extract leftmost digit
    int right = in % 10;          // Extract rightmost digit

    if (left != right) {
        return false;             // If digits don't match, it's not a palindrome
    }

    // Remove the leftmost and rightmost digits and check the remaining part
    int temp = in - left * cal_power;
    temp = temp / 10;             // Remove rightmost digit
    return palindrome(temp, len - 2);
}

// Main function to determine if the input is a palindrome
int main() {
    int in = 12321; // Input number
    int ten = 10;
    int index = 1;

    // Determine the number of digits (len)
    for (index = 1;; ++index) {
        int cal_power = cal_pow(ten, index);
        int d = in / cal_power;
        if (d == 0) {
            break; // Stop when no more digits are left
        }
    }

    int exp = index - 1; // Length of the number minus one
    printf("%d\n", palindrome(in, exp)); // Print 1 for true, 0 for false

    return 0;
}

