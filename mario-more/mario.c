#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //get height 1 to 8
    int h, r, space, brick1, brick2;
    do
    {
        h = get_int("Height (1 to 8): ");
    }
    while (h < 1 || h > 8);

    //for each row of stairs
    for (r = 1; r <= h; r++)
    {
        //print left half of empty space
        for (space = 0; space < h - r; space++)
        {
            printf(" ");
        }

        //print left half of bricks
        for (brick1 = 0; brick1 < r; brick1++)
        {
            printf("#");
        }

        //print middle empty space
        printf("  ");

        //print right half of bricks
        for (brick2 = 0; brick2 < r; brick2++)
        {
            printf("#");
        }

        //go to next row
        printf("\n");
    }

}