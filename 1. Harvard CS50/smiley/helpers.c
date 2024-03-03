#include "helpers.h"
#include <stdio.h>

void colorize(int height, int width, RGBTRIPLE image[height][width])
{
    // Change all black pixels to a color of your choosing
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            RGBTRIPLE pixel = image[i][j];
            if (pixel.rgbtBlue == 0x00 && pixel.rgbtGreen == 0x00 && pixel.rgbtRed == 0x00)
            {
                image[i][j].rgbtBlue = 0x96;
            }
        }
    }
}
