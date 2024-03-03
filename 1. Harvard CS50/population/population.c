#include <cs50.h>
#include <stdio.h>

int calcYears(int start, int end);
int getStart();
int getEnd();

int main(void)
{
    // TODO: Prompt for start size
    int startSize = getStart();

    // TODO: Prompt for end size
    int endSize = getEnd(startSize);

    // TODO: Calculate number of years until we reach threshold
    int years = calcYears(startSize, endSize);

    // TODO: Print number of years
    printf("Years: %i\n", years);
}

int calcYears(int start, int end)
{
    int years = 0;
    while (start < end)
    {
        start = start + (start / 3) - (start / 4);
        years++;
    }
    return years;
}

int getStart(int startSize)
{
    do
    {
        startSize = get_int("Start size: ");
        if (startSize < 9)
        {
            printf("The population size need to be greater or equal to 9!\n");
        }
    }
    while (startSize < 9);

    return startSize;
}

int getEnd(int endSize, int startSize)
{
    do
    {
        endSize = get_int("End size: ");
        if (endSize < startSize)
        {
            printf("The end size need to be greater than the start size!\n");
        }
    }
    while (endSize < startSize);

    return endSize;
}
