#include <stdio.h>
#include <stdlib.h>

// Compute the integer square root of a number
int sqrt_int(int x) {
    int i = 1;
    for (i = 1; i * i <= x; ++i) {
        // Increment i while i^2 <= x
    }
    return i - 1; // Return the largest integer where (i-1)^2 <= x
}

// Function to compute the roots of the quadratic equation ax^2 + bx + c = 0
void quadratic(int a, int b, int c) {
    int discriminant = b * b - 4 * a * c; // Compute discriminant
    if (discriminant < 0) {
        printf("No real roots\n"); // No real roots if discriminant is negative
        return;
    }

    int sqrt_d = sqrt_int(discriminant); // Compute integer square root of discriminant
    int denominator = 2 * a; // Compute denominator

    // Compute first root
    int root1 = (-b + sqrt_d) / denominator;
    printf("%d\n", root1);

    // Compute second root
    int root2 = (-b - sqrt_d) / denominator;
    printf("%d\n", root2);
}

int main() {
    int a = -5;  // Coefficient of x^2
    int b = 8;   // Coefficient of x
    int c = 21;  // Constant term

    quadratic(a, b, c); // Solve the quadratic equation
    return 0;
}
