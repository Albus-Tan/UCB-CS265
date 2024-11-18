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
    z *= 20;
    printf("%d\n", z);

    int a = 20;
    int b = 2;
    int m = 3;
    int div = a / b;
    printf("%d\n", div);
    int mod = a % m;
    printf("%d\n", mod);
    int mul = a * b;
    printf("%d\n", mul);
    int add = div + mul;
    printf("%d\n", add);
    int sub = div - mul;
    printf("%d\n", sub);

    int neg = -a;
    printf("%d\n", neg);
}
