#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main() {
    char text[100];
    int key[2][2] = {{3, 3}, {2, 5}};

    printf("Enter plaintext: ");
    scanf("%s", text);

    int len = strlen(text);

    if (len % 2 != 0) {
        text[len] = 'X';
        text[len + 1] = '\0';
        len++;
    }

    printf("Encrypted Text: ");

    for (int i = 0; i < len; i += 2) {
        int a = toupper(text[i]) - 'A';
        int b = toupper(text[i + 1]) - 'A';

        int c1 = (key[0][0] * a + key[0][1] * b) % 26;
        int c2 = (key[1][0] * a + key[1][1] * b) % 26;

        printf("%c%c", c1 + 'A', c2 + 'A');
    }

    printf("\n");

    return 0;
}