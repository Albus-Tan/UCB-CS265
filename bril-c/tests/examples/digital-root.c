#include <stdio.h>

// Peel the last digit of a number
int peel_last_digit(int input) {
    return input % 10;
}

// Compute the digital root of a number
int digital_root(int input) {
    int result = 0;

    for (; input > 0 || result >= 10;) {
        if (input == 0) {
            input = result;
            result = 0;
        }

        int digit = peel_last_digit(input);
        input /= 10;
        result += digit;
    }

    return result;
}

int main() {
    int input = 645634654; // Input argument

    int result = digital_root(input);
    printf("%d\n", result); // Print the digital root

    return 0;
}
