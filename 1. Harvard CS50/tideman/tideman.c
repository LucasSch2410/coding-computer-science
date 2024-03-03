#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
} pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);
bool creates_cycle(int start, int end);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i], name) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }

    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]]++;
        }
    }
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;
            }
        }
    }
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // TODO - Bubble Sort
    // Verify if i = 1 breaks the code
    int i = 1;

    if (pair_count > 2)
    {
        i = pair_count - 1;
    }

    int winner, loser, firstPair, secondPair;
    pair nextPair;

    while (i > 0)
    {
        for (int j = 0; j < pair_count - 1; j++)
        {

            winner = preferences[pairs[j].winner][pairs[j].loser];
            loser = preferences[pairs[j].loser][pairs[j].winner];

            firstPair = winner - loser;

            winner = preferences[pairs[j + 1].winner][pairs[j + 1].loser];
            loser = preferences[pairs[j + 1].loser][pairs[j + 1].winner];

            secondPair = winner - loser;

            if (secondPair > firstPair)
            {
                nextPair = pairs[j + 1];

                pairs[j + 1] = pairs[j];

                pairs[j] = nextPair;
            }
        }

        i--;
    }
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // TODO
    for (int i = 0; i < pair_count; i++)
    {
        // Winner create the arrow, the loser recieves the arrow pointing to him
        if (!creates_cycle(pairs[i].winner, pairs[i].loser))
        {
            locked[pairs[i].winner][pairs[i].loser] = true;
        }
    }
}

// Print the winner of the election
void print_winner(void)
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        int arrows_count = 0;
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[j][i])
            {
                arrows_count++;
            }
        }
        if (arrows_count == 0)
        {
            printf("%s\n", candidates[i]);
            return;
        }
    }
}

bool creates_cycle(int start, int end)
{
    if (start == end)
    {
        return true;
    }

    for (int i = 0; i < candidate_count; i++)
    {
        // Check if the locked[end] have nodes, so calls the creates_cycle
        // To that node until doesn't have more nodes.
        if (locked[end][i] && creates_cycle(start, i))
        {
            return true;
        }
    }

    return false;
}
