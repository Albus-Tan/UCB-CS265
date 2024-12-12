#include <stdio.h>
#include <stdbool.h>

int main() {
    for (int i = 0; i < 10; i++){
        if (i == 5) continue;
        printf("%d\n", i);
        for (int j = 0; j < 10; j++){
            printf("%d\n", j);
            if (j == 5) break;
        }
    }
}
