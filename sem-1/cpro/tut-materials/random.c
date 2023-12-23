#include <stdio.h>
#include <stdlib.h>

int main()
{
    srand(100);
    double x, y;
    x = (double)rand() / RAND_MAX;
    y = (double)rand() / RAND_MAX;
    printf("%f\n", x);
    printf("%f\n", y);
    for (int i = 0; i < 4; i++)
        printf("%d\n", rand());
    return 0;
}