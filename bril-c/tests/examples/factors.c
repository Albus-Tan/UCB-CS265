#include <stdio.h>

// Prints the integer factors of a number using trial division
void print_factors(int num) {
    int fac = 2; // Start with the smallest prime factor

    for (; num > 1;) { // Continue until the number is fully factored
        int quo = num / fac;
        int mod = num - quo * fac; // Equivalent to num % fac

        if (mod == 0) {
            printf("%d\n", fac); // Print the factor
            num = num / fac;    // Reduce the number
        } else {
            fac = fac + 1;      // Increment the factor
        }
    }
}

int main() {
    int num = 60; // Input number
    print_factors(num);
    return 0;
}
