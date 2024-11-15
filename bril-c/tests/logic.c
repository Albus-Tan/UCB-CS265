#include <stdio.h>
#include <stdbool.h>

int main() {
    bool x = true;
    bool y = false;
    bool and = x && y;
    bool or = x || y;

    // Logic tests
    printf("%d\n", and);
    printf("%d\n", or);
    printf("%d\n", !x);
    printf("%d\n", !y);
}
