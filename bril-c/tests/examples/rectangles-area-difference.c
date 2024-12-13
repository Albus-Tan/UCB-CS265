#include <stdio.h>

// Function to compute and return the area of a rectangle
int area(int x, int y) {
    int result = x * y;
    printf("%d\n", result); // Print the area of the rectangle
    return result;
}

int main() {
    int x1 = 5;
    int y1 = 10;   // Dimensions of the first rectangle
    int x2 = 6;
    int y2 = 13;   // Dimensions of the second rectangle

    // Compute the areas of the two rectangles
    int a1 = area(x1, y1);
    int a2 = area(x2, y2);

    // Compute the difference in areas
    int res = a1 - a2;

    // Ensure the result is non-negative
    if (a1 < a2) {
        res = -res;
    }

    // Print the absolute difference
    printf("%d\n", res);

    return 0;
}
