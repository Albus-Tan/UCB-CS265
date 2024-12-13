#include <stdio.h>

// Recursive implementation of the Ackermann function
int ack(int m, int n) {
    if (m == 0) {
        return n + 1;
    } else if (n == 0) {
        return ack(m - 1, 1);
    } else {
        return ack(m - 1, ack(m, n - 1));
    }
}

int main() {
    int m = 3;
    int n = 6;

    int result = ack(m, n);

    printf("%d\n", result);

    return 0;
}
