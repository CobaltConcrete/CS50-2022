#include "helpers.h"
#include <stdio.h>
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    //for each bmp pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red = image[i][j].rgbtRed;
            int green = image[i][j].rgbtGreen;
            int blue = image[i][j].rgbtBlue;

            //round float_average to nearest int
            int average = round((red + green + blue) / 3.0);
            image[i][j].rgbtRed = image[i][j].rgbtGreen = image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
int round_and_cap255(float f);

void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    //for each pixel in bmp
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float sepiaRed = .393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue;
            float sepiaGreen = .349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue;
            float sepiaBlue = .272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue;

            //round float_sepia to nearest int
            image[i][j].rgbtRed = round_and_cap255(sepiaRed);
            image[i][j].rgbtGreen = round_and_cap255(sepiaGreen);
            image[i][j].rgbtBlue = round_and_cap255(sepiaBlue);
        }
    }
    return;
}

int round_and_cap255(float f)
{
    int color;
    color = round(f);
    color = color > 255 ? 255 : color;
    return color;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //for each bmp pixel on left-half of image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0, halfwidth = width / 2; j < halfwidth; j++)
        {
            //swap with bmp pixel on right-half of image
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = temp;
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int pixel;
    float sumR, sumG, sumB;
    pixel = 0;
    sumR = sumG = sumB = 0;
    RGBTRIPLE original[height][width];

    //make copy of bmp image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            original[i][j] = image[i][j];
        }
    }

    //for each main pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //for each of surrounding pixels
            for (int x = i - 1; x <= i + 1; x++)
            {
                for (int y = j - 1; y <= j + 1; y++)
                {
                    //if surrounding pixels are within image dimensions
                    if (x >= 0 && x < height && y >= 0 && y < width)
                    {
                        sumR += original[x][y].rgbtRed;
                        sumG += original[x][y].rgbtGreen;
                        sumB += original[x][y].rgbtBlue;
                        pixel++;
                    }

                }
            }

            //find float_average of color based on no. of pixels used, then round to nearest int
            image[i][j].rgbtRed = round(sumR / pixel);
            image[i][j].rgbtGreen = round(sumG / pixel);
            image[i][j].rgbtBlue = round(sumB / pixel);
            pixel = 0;
            sumR = sumG = sumB = 0;
        }
    }

    return;
}