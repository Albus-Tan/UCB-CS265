#include <stdio.h>
#include <stdbool.h>

int main() {
   int lowerBound = 1;
   int upperBound = 500;

   int number = 0;
   if (lowerBound < 2) {
       number = 2;
   } else {
       number = lowerBound;
   }

   for (; number <= upperBound; number++) {
       bool isPrime = true;
       for (int divisor = 2; divisor <= number / 2; divisor++) {
           int remainder = number - (number / divisor) * divisor;
           if (remainder == 0) {
               isPrime = false;
            //    break;
           }
       }
       if (isPrime) {
           printf("%d\n", number);
       }
   }
}
