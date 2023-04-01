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

// Detect edges
int round_and_cap255(float f);

void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE original[height][width];
    float gxr, gxg, gxb, gyr, gyg, gyb, RedFloat, GreenFloat, BlueFloat;
    gxr = gxg = gxb = gyr = gyg = gyb = 0;

    //gx kernel values
    int gx[3][3] =
    {
        {-1, 0, 1},
        {-2, 0, 2},
        {-1, 0, 1}
    };

    //gy kernel values
    int gy[3][3] =
    {
        {-1, -2, -1},
        { 0,  0,  0},
        { 1,  2,  1}
    };

    //create copy of bmp file
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            original[i][j] = image[i][j];
        }
    }

    //for each main-pixel in bmp
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //reset gx and gy sums
            gxr = gxg = gxb = gyr = gyg = gyb = 0;

            //for each kernel-pixel of main-pixel
            for (int x = i - 1; x <= i + 1; x++)
            {
                for (int y = j - 1; y <= j + 1; y++)
                {
                    // kernel coordinates:
                    // {[i-1][j-1], [i-1][j], [i-1][j+1]},
                    // {[i]  [j-1], [i]  [j], [i]  [j+1]},
                    // {[i+1][j-1], [i+1][j], [i+1][j+1]}

                    //if kernel-pixel is within bmp parameters
                    if (x >= 0 && x < height && y >= 0 && y < width)
                    {
                        //let gx[a][b] and gy[a][b]

                        int a = x - i + 1;
                        int b = y - j + 1;

                        //multiply color by kernel value
                        gxr += gx[a][b] * original[x][y].rgbtRed;
                        gxg += gx[a][b] * original[x][y].rgbtGreen;
                        gxb += gx[a][b] * original[x][y].rgbtBlue;
                        gyr += gy[a][b] * original[x][y].rgbtRed;
                        gyg += gy[a][b] * original[x][y].rgbtGreen;
                        gyb += gy[a][b] * original[x][y].rgbtBlue;
                    }

                }
            }

            RedFloat = sqrt(gxr * gxr + gyr * gyr);
            GreenFloat = sqrt(gxg * gxg + gyg * gyg);
            BlueFloat = sqrt(gxb * gxb + gyb * gyb);

            image[i][j].rgbtRed = round_and_cap255(RedFloat);
            image[i][j].rgbtGreen = round_and_cap255(GreenFloat);
            image[i][j].rgbtBlue = round_and_cap255(BlueFloat);
        }
    }
    return;
}

//round float to nearest int and cap at 255
int round_and_cap255(float f)
{
    int color;
    color = round(f);
    color = color > 255 ? 255 : color;
    return color;
}
