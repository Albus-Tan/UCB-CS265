#include <stdio.h>

// Compute x^n using recursion
int cal_pow(int x, int n) {
    if (n == 1) {
        return x;
    }
    int half = cal_pow(x, n / 2);
    int half2 = half * half;
    if (n % 2 == 1) {
        return half2 * x;
    } else {
        return half2;
    }
}

// Perform left shift operation (x << step)
int LEFTSHIFT(int x, int step) {
    return x * cal_pow(2, step);
}

// Perform right shift operation (x >> step)
int RIGHTSHIFT(int x, int step) {
    return x / cal_pow(2, step);
}

// Main function
int main() {
    int a = 3;
    int b = 5;
    int c = 10000;
    int d = 4;

    int ans1 = LEFTSHIFT(a, b);
    printf("%d\n", ans1);

    int ans2 = RIGHTSHIFT(c, d);
    printf("%d\n", ans2);

    return 0;
}
