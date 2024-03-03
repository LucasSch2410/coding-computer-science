#include <cs50.h>
#include <stdio.h>

// Asks the name and return hello
int main(void)
{
    string name = get_string("What's your name? ");

    printf("hello, %s\n", name);
}
