#include <cs50.h>
#include <stdio.h>

int calculateCard(long card);
void verifyCard(int checkSum, long card);

int main(void)
{
    // Prompt for input
    long card = get_long("Diga: ");

    // Calculate checksum
    int checkSum = calculateCard(card);

    // Check for card length and starting digits
    verifyCard(checkSum, card);
}

int calculateCard(long card)
{
    int length = 0;
    long totalSum = 0;
    long digit = 0;

    // Calculates the digits of the card
    for (long i = 10; digit != card; i *= 10)
    {
        // Add the length of the card
        length++;

        // Defines and calculates the digits
        digit = card % i;

        long firstSum = 0;
        long oddSum = 0;

        if (length % 2)
        {
            oddSum = digit / (i / 10);
        }
        else
        {
            long evenNumber = (digit / (i / 10)) * 2;

            if (evenNumber >= 10)
            {
                firstSum = firstSum + ((evenNumber / 10) + (evenNumber % 10));
            }
            else
            {
                firstSum = firstSum + evenNumber;
            }
        }

        // Calculates the final result
        totalSum = totalSum + (firstSum + oddSum);
        printf("%li\n", totalSum);
    }
    return totalSum;
}

void verifyCard(int checkSum, long card)
{
    int length = 0;
    long digit = 0;
    long i = 10;
    for (; digit != card; i *= 10)
    {
        length++;
        digit = card % i;
    }

    if (length > 12 && length < 17 && checkSum % 10 == 0)
    {
        long firstNumbers = digit / (i / 1000);
        if ((firstNumbers == 34 || firstNumbers == 37) && length == 15)
        {
            printf("AMEX\n");
        }
        else if (firstNumbers > 50 && firstNumbers < 56 && length == 16)
        {
            printf("MASTERCARD\n");
        }
        else if (firstNumbers >= 40 && firstNumbers < 50 && (length == 13 || length == 16))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}
