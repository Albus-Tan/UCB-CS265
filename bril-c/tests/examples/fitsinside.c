#include <stdio.h>
#include <stdbool.h>

// Check if the first rectangle fits inside the second
bool fitsInside(int w1, int h1, int w2, int h2) {
    // Check if the rectangle fits without rotation
    bool first_check = (w1 <= w2) && (h1 <= h2);

    // Check if the rectangle fits with rotation
    bool second_check = (w1 <= h2) && (h1 <= w2);

    // Return true if either condition is satisfied
    return first_check || second_check;
}

int main() {
    int width1 = 12;   // Width of first rectangle
    int height1 = 4;   // Height of first rectangle
    int width2 = 5;    // Width of second rectangle
    int height2 = 13;  // Height of second rectangle

    // Check if the first rectangle fits inside the second
    bool output = fitsInside(width1, height1, width2, height2);

    // Print the result
    printf("%d\n", output);

    return 0;
}
