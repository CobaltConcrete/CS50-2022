// Implements a dictionary's functionality

#include <stdio.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 2881;

// Hash table
node *table[N];

int wordcount = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int hashvalue = hash(word);
    node *cursor = table[hashvalue];

    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }

        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int sum = 0;
    int n = strlen(word);

    for (int i = 0; i < n; i++)
    {
        sum += tolower(word[i]);
    }
    return sum % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    char word[LENGTH + 1];

    //open dictionary
    FILE *dict = fopen(dictionary, "r");

    if (dictionary == NULL)
    {
        return false;
    }

    //scan each word in dictionary until End Of File
    while (fscanf(dict, "%s", word) != EOF)
    {
        node *temp = malloc(sizeof(node));
        if (temp == NULL)
        {
            return false;
        }

        //copy word from dict to node *temp->word
        strcpy(temp->word, word);
        temp->next = NULL;

        //give word a hash value
        int hashvalue = hash(word);

        //if node *table[hashvalue] is empty, place new word in table[hashvalue]->word
        if (table[hashvalue] == NULL)
        {
            table[hashvalue] = temp;
        }

        //else move pointer to temp->next pointer to start of table[hashvalue]->word, update table[hashvalue]->word = new word
        else
        {
            temp->next = table[hashvalue];
            table[hashvalue] = temp;
        }

        //update number of words
        wordcount++;
    }

    //close dictionary file
    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return wordcount;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *pointer = table[i];

        //while node is not empty
        while (pointer != NULL)
        {
            //free node *(pointer->word), then update so that the old (pointer->next) is now the new (pointer->word), repeat
            node *temp = pointer;
            pointer = pointer->next;
            free(temp);
        }

        //if node is empty and node *pointer = node *table[last]
        if (pointer == NULL && i == N - 1)
        {
            return true;
        }
    }
    return false;
}
