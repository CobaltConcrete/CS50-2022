#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int h, r, space, brick;

    //get height 1 to 8
    do
    {
        h = get_int("Height (1 to 8): ");
    }
    while (h < 1 || h > 8);

    //for each row of stairs
    for (r = 1; r <= h; r++)
    {
        //print empty space before bricks
        for (space = 0; space < h - r; space++)
        {
            printf(" ");
        }

        //print bricks
        for (brick = 0; brick < r; brick++)
        {
            printf("#");
        }

        //go to next row
        printf("\n");
    }

}