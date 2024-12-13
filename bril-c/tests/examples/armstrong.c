#include <stdio.h>
#include <stdbool.h>

// Function to compute the number of digits in n
int getDigits(int n) {
    int digits = 0;
    for (; n > 0; n /= 10) {
        digits++;
    }
    return (digits == 0) ? 1 : digits; // Handle case when n == 0
}

// Function to compute base^exp
int cal_pow(int base, int exp) {
    int result = 1;
    for (int i = 0; i < exp; ++i) {
        result *= base;
    }
    return result;
}

// Main function to check if the input is an Armstrong number
void checkArmstrong(int input) {
    int tmp = input;
    int sum = 0;
    int digits = getDigits(input);

    for (; tmp > 0; tmp /= 10) {
        int digit = tmp % 10;         // Extract the last digit
        sum += cal_pow(digit, digits); // Add its digits^digits
    }

    // Compare the sum of powered digits with the original number
    bool isArmstrong = (sum == input);
    printf("%d\n", isArmstrong);
}

int main() {
    int input = 407; // Input value
    checkArmstrong(input);
    return 0;
}
