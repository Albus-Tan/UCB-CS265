#include <stdio.h>

int fact(int a) {
    if (a == 0) {
        return 1;
    } else {
        return a * fact(a - 1);
    }
}

int main() {
    int a = 5;
    int x = fact(a);
    printf("%d\n", x);
}
