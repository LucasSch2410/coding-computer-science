#include <cs50.h>
#include <stdio.h>

int getHeight(void);
void printPyramid(int height);

// Asks a height and returns a pyramid
int main(void)
{
    // TODO: prompt the height of pyramid
    int height = getHeight();

    // TODO: print the pyramid
    printPyramid(height);
}

int getHeight(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height > 8 || height < 1);
    return height;
}

void printPyramid(int height)
{
    for (int i = 0; i < height; i++)
    {
        // Print the spaces only if the height is above of 1
        for (int space = 0; space < height - 1 - i; space++)
        {
            printf(" ");
        }

        // Print left pyramid
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        printf("  ");

        // Print right pyramid
        for (int k = 0; k <= i; k++)
        {
            printf("#");
        }

        // New column
        printf("\n");
    }
}