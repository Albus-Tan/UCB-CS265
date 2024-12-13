#include <stdio.h>

// Compute the greatest common divisor (GCD) of a and b
int gcd(int a, int b) {
    for (; b != 0;) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

int main() {
    int x = 23789216;      // First number
    int y = 1748698766;    // Second number

    int result = gcd(x, y); // Compute GCD
    printf("%d\n", result); // Print the result

    return 0;
}
