#include <stdio.h>
#include <stdbool.h>

int main() {
    int x = 5;
    int y = 1;
    int z = 0;
    bool t = true;
    bool f = false;
    if (t)
        printf("%d\n", x);
    else
        printf("%d\n", y);
    if (x < z)
    {
        printf("%d\n", x);
    }
    else
    {
        if (f)
            printf("%d\n", x);
        else
            printf("%d\n", y);
        printf("%d\n", y);
    }
}
