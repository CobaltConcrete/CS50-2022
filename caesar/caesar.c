#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
        return 1;
        }
    }

    int key = atoi(argv[1])%26;

    string p = get_string("plaintext:  ");
    printf("ciphertext: ");

    for (int x = 0; x < strlen(p); x++)
    {
        char c = p[x];

        if (isupper(p[x]))
        {
            printf("%c", (c - 65 + key) % 26 + 65);
        }
        else if (islower(p[x]))
        {
            printf("%c", (c - 97 + key) % 26 + 97);
        }
        else
        {
            printf("%c", c);
        }

    }

    printf("\n");

}

