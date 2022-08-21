#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n, i, j;
    //Do
    do
    {
        //User input
        n = get_int("What's the height: ");
    }
    //Inside of codition
    //Loop until to find the break
    while ((n < 1) || (n > 8));

    //With a loop for each row
    for (i = 0; i < n; i++)
    {
        // With a loop for each spaces
        for (j = n - i; j > 1; j--)
        {
            printf(" ");
        }
        // With a loop for column
        for (j = 0; j <= i; j++)
            //Print a brick
        {
            printf("#");
        }
        // Move to next row
        printf("\n");
    }
}