    #include <stdio.h>
    
    int main()
    {
        int i = 0;
        int sum = 0;
       
        for ( i = 1; i <= 100; i++ ) {
          sum += i;
        }
        printf("%d\n", sum);

        return 0;
    }

