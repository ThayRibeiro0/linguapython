#include <stdio.h>

int main(void)
{
    FILE *file = fopen("phonebook.csv", "a");
    if (!file)
    {
        return 1;
    }

    string name = get_string("Name: ");
    string number = get_string("Number: ");
}