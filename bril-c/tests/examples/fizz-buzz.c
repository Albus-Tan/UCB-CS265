#include <stdio.h>
#include <stdbool.h>

// FizzBuzz implementation
void fizzbuzz(int input) {
    for (int index = 1; index < input; ++index) {
        int div3 = index / 3;
        int mod3 = div3 * 3;
        bool isFizz = (mod3 == index);

        int div5 = index / 5;
        int mod5 = div5 * 5;
        bool isBuzz = (mod5 == index);

        if (isFizz && isBuzz) {
            printf("%d\n", -1);  // FizzBuzz
        } else if (isFizz) {
            printf("%d\n", -2);  // Fizz
        } else if (isBuzz) {
            printf("%d\n", -3);  // Buzz
        } else {
            printf("%d\n", index);  // Number
        }
    }
}

int main() {
    int input = 101;
    fizzbuzz(input);
    return 0;
}

