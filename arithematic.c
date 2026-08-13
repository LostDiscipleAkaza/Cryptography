#include <stdio.h>

int main() {
    int a, b, ch;

    printf("Enter first number\nEnter second number\nEnter choice\n\n");
    printf("1. Addition\n2. Subtraction\n3. Multiplication\n4. Division\n5. Modulus\n\n");

    scanf("%d %d %d", &a, &b, &ch);

    switch (ch) {
        case 1:
            printf("Addition : %d\n", a + b);
            break;

        case 2:
            printf("Substraction : %d\n", a - b);
            break;

        case 3:
            printf("Multiplication : %d\n", a * b);
            break;

        case 4:
            if (b != 0) {
                printf("Division : %f\n", (float)a / b);
            } else {
                printf("division by zero is invalid\n");
            }
            break;

        case 5:
            printf("Modulus : %d\n", a % b);
            break;

        default:
            printf("Enter between 1 to 5");
            break;
    }

    return 0;
}