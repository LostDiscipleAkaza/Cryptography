#include <stdio.h>
#include <stdlib.h>

int gcd(int a, int b)
{
    a = abs(a);
    b = abs(b);
    if (a == 0 && b == 0)
    {
        printf("GCD is undefined.\n");
        exit(1);
    }
    while (b != 0)
    {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}
int main()
{
    int a, b;
    printf("Enter two integers: ");
    scanf("%d %d", &a, &b);

    printf("GCD = %d\n", gcd(a, b));

    return 0;
}