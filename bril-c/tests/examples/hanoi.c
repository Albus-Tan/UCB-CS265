#include <stdio.h>

// Recursive function to solve Tower of Hanoi
void hanoi(int disks, int src, int dst, int spare) {
    if (disks > 0) {
        int above = disks - 1;

        // Move n-1 disks from src to spare using dst as spare
        hanoi(above, src, spare, dst);

        // Move the nth disk from src to dst
        printf("%d\n", src);
        printf("%d\n", dst);

        // Move n-1 disks from spare to dst using src as spare
        hanoi(above, spare, dst, src);
    }
}

int main() {
    int disks = 3; // Number of disks

    int src = 0;   // Source rod
    int dst = 2;   // Destination rod
    int spare = 1; // Spare rod

    // Solve Tower of Hanoi
    hanoi(disks, src, dst, spare);

    return 0;
}
