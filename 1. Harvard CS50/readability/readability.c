#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
void calculates_class(string text);

int main(void)
{
    // Get the text.
    string text = get_string("Text: ");

    calculates_class(text);
}

int count_letters(string text)
{

    int letters = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }

    return letters;
};

int count_words(string text)
{
    int words = 0;
    int i = 0;

    while (i < strlen(text))
    {
        if (isblank(text[i]))
        {
            words++;
        };

        i++;
    }

    if (words > 0)
    {
        words++;
    }

    return words;
}

int count_sentences(string text)
{
    int sentences = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == 21 || text[i] == 63 || text[i] == 46)
        {
            sentences++;
        }
    }

    return sentences;
}

void calculates_class(string text)
{
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    float L = 100 * ((float) letters / (float) words);
    float S = 100 * ((float) sentences / (float) words);

    int index = (int) round(0.0588 * L - 0.296 * S - 15.8);

    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}
