#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            RGBTRIPLE pixel = image[i][j];
            int average = round((pixel.rgbtBlue + pixel.rgbtGreen + pixel.rgbtRed) / 3.0);
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE inverseRow[1][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = width - 1, k = 0; k < width; j--, k++)
        {
            inverseRow[0][k].rgbtBlue = image[i][j].rgbtBlue;
            inverseRow[0][k].rgbtGreen = image[i][j].rgbtGreen;
            inverseRow[0][k].rgbtRed = image[i][j].rgbtRed;
        }

        for (int l = 0; l < width; l++)
        {
            image[i][l].rgbtBlue = inverseRow[0][l].rgbtBlue;
            image[i][l].rgbtGreen = inverseRow[0][l].rgbtGreen;
            image[i][l].rgbtRed = inverseRow[0][l].rgbtRed;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];

    for (int a = 0; a < height; a++)
    {
        for (int b = 0; b < width; b++)
        {
            copy[a][b] = image[a][b];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int averageRed = 0, averageBlue = 0, averageGreen = 0;
            int countpixels = 0;

            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int avDi = i + di;
                    int avDj = j + dj;

                    if (avDi >= 0 && avDi < height && avDj >= 0 && avDj < width)
                    {
                        averageRed += copy[avDi][avDj].rgbtRed;
                        averageBlue += copy[avDi][avDj].rgbtBlue;
                        averageGreen += copy[avDi][avDj].rgbtGreen;

                        countpixels++;
                    }
                }
            }

            image[i][j].rgbtRed = round((float) averageRed / countpixels);
            image[i][j].rgbtBlue = round((float) averageBlue / countpixels);
            image[i][j].rgbtGreen = round((float) averageGreen / countpixels);
        }
    }
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{

    RGBTRIPLE copy[height][width];
    int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    for (int a = 0; a < height; a++)
    {
        for (int b = 0; b < width; b++)
        {
            copy[a][b] = image[a][b];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int averageRedGx = 0, averageBlueGx = 0, averageGreenGx = 0;
            int averageRedGy = 0, averageBlueGy = 0, averageGreenGy = 0;
            int countpixels = 0;

            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int avDi = i + di;
                    int avDj = j + dj;

                    if (avDi >= 0 && avDi < height && avDj >= 0 && avDj < width)
                    {
                        averageRedGx += gx[di + 1][dj + 1] * copy[avDi][avDj].rgbtRed;
                        averageBlueGx += gx[di + 1][dj + 1] * copy[avDi][avDj].rgbtBlue;
                        averageGreenGx += gx[di + 1][dj + 1] * copy[avDi][avDj].rgbtGreen;

                        averageRedGy += gy[di + 1][dj + 1] * copy[avDi][avDj].rgbtRed;
                        averageBlueGy += gy[di + 1][dj + 1] * copy[avDi][avDj].rgbtBlue;
                        averageGreenGy += gy[di + 1][dj + 1] * copy[avDi][avDj].rgbtGreen;
                    }
                }
            }

            int newChannelRed = round(sqrt(pow(averageRedGx, 2) + pow(averageRedGy, 2)));
            int newChannelBlue = round(sqrt(pow(averageBlueGx, 2) + pow(averageBlueGy, 2)));
            int newChannelGreen = round(sqrt(pow(averageGreenGx, 2) + pow(averageGreenGy, 2)));

            if (newChannelRed > 255)
            {
                newChannelRed = 255;
            }

            if (newChannelBlue > 255)
            {
                newChannelBlue = 255;
            }

            if (newChannelGreen > 255)
            {
                newChannelGreen = 255;
            }

            image[i][j].rgbtRed = newChannelRed;
            image[i][j].rgbtBlue = newChannelBlue;
            image[i][j].rgbtGreen = newChannelGreen;
        }
    }
}
