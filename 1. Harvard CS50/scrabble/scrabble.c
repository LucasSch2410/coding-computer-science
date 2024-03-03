#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);
void compute_winner(int score1, int score2);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // TODO: Print the winner
    compute_winner(score1, score2);
}

int compute_score(string word)
{
    // TODO: Compute and return score for string

    int wordValues[strlen(word)];
    int score = 0;

    for (int i = 0; i < strlen(word); i++)
    {

        // Verify if the letter is a valid character
        if (toupper(word[i]) < 91 && toupper(word[i]) > 64)
        {
            wordValues[i] = toupper(word[i]);
        }
        else
        {
            wordValues[i] = 0;
        }

        score += POINTS[wordValues[i] - 65];
    }

    return score;
}

void compute_winner(int score1, int score2)
{
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}
