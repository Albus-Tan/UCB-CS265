#include <stdio.h>

// Recursively print the binary representation of n
void printBinary(int n) {
    if (n == 0) {
        return;
    }
    int v0 = n % 2;
    int v1 = n / 2;
    printBinary(v1);
    printf("%d\n", v0);
}

int main() {
    int n = 128;
    printBinary(n);
}
