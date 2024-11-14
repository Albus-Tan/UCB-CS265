#include <stdio.h>

int main() {
    int x = 5;
    int y = 1;
    x += y;
    printf("%d\n", x);
    x -= y;
    printf("%d\n", x);

    int z = 10;
    z /= x;
    printf("%d\n", z);

    int a = 20;
    int b = 2;
    int div =  a/b;
    printf("%d\n", div);
}
