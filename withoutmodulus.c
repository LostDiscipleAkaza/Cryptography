#include <stdio.h>
#include <stdlib.h>

int modulus(int a, int b)
{
    if (b == 0)
    {
        printf("Error: Modulus by zero is not allowed.\n");
        exit(1);
    }

    int rem = a - (a / b) * b;
    return rem;
}

int main()
{
    int a, b;

    printf("Enter two integers: ");
    scanf("%d %d", &a, &b);

    printf("Modulus of %d and %d = %d\n", a, b, modulus(a, b));

    return 0;
}