#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    FILE *image = NULL;
    typedef uint8_t BYTE;
    BYTE buffer[512];
    int number = 0;
    char *filename = malloc(8*sizeof(char));

    if (argc != 2)
    {
        printf("Usage: ./recover filename\n");
        return 1;
    }

    //if cannot open file
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Error opening file.\n");
        return 1;
    }

    while (fread(buffer, sizeof(BYTE), 512, file) == 512)
    {
        //if start of a jpg
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //if not first jpg
            if(number != 0)
            {
                //close previous jpg
                fclose(image);
            }

            //create image file, write into it, then increase file number
            sprintf(filename, "%03i.jpg", number);
            image = fopen(filename, "w");
            fwrite(buffer, sizeof(BYTE), 512, image);
            number++;
        }

        //if not start of but is part of jpg
        else if(number != 0)
        {
            fwrite(buffer, sizeof(BYTE), 512, image);
        }
    }

    fclose(file);
    fclose(image);
    free(filename);
    return 0;
}