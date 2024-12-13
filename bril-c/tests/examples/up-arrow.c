#include <stdio.h>

// Function to compute up-arrow notation
int up_arrow(int num, int arrows, int repeats) {
    int ans = num;

    for (int i = 1; i < repeats; ++i) {
        if (arrows <= 1) {
            // Base case: single arrow means repeated multiplication
            ans *= num;
        } else {
            // Recursive case: reduce the number of arrows
            ans = up_arrow(num, arrows - 1, ans);
        }
    }

    return ans;
}

int main() {
    int n = 2;        // Base
    int arrows = 3;   // Number of arrows
    int repeats = 3;  // Repeats

    // Compute the result of the up-arrow notation
    int ans = up_arrow(n, arrows, repeats);
    printf("%d\n", ans); // Print the result

    return 0;
}
