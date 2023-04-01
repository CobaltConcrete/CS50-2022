#include <stdio.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

int main()
{
    char word[LENGTH + 1];

    //open dictionary
    FILE *dict = fopen(dictionary, "r");

    if (dictionary == NULL)
    {
    return false;
    }

    long sum = 0;
    long wordcount = 0;

    //scan each word in dictionary until End Of File
    while (fscanf(dict, "%s", word) != EOF)
    {
        int n = strlen(word);

        for (int i = 0; i < n; i++)
        {
            sum += tolower(word[i]);
        }
        wordcount++;
    }

    printf("%li", sum/wordcount);

}