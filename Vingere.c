#include <stdio.h>
#include <string.h>
#include <ctype.h>

void encrypt(char text[], char key[]) {
    int len = strlen(text);
    int keyLen = strlen(key);

    printf("Encrypted Text: ");

    for (int i = 0; i < len; i++) {
        char ch = toupper(text[i]);

        if (ch >= 'A' && ch <= 'Z') {
            int p = ch - 'A';
            int k = toupper(key[i % keyLen]) - 'A';
            char c = (p + k) % 26 + 'A';
            printf("%c", c);
        }
    }

    printf("\n");
}

int main() {
    char text[100], key[100];

    printf("Enter plaintext: ");
    scanf("%s", text);

    printf("Enter key: ");
    scanf("%s", key);

    encrypt(text, key);

    return 0;
}