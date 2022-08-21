from sys import argv
from sys import exit
import csv

def main():

    # TODO: Check for command-line usage
    longest_str = {}

    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py database.csv sequence.txt")

    # TODO: Read database file into a variable
    info = []
    str_sequence = []
    sequence = []

    base = sys.argv[1]

    with open(base) as f:
        reader = csv.DictReader(f)

        for name in reader:
            info.append(name)

    # TODO: Read DNA sequence file into a variable
    txt = sys.argv[2]
    sequence = txt.read()

    # TODO: Find longest match of each STR in DNA sequence
    counts = dict.fromkeys(str_sequence, 0)

    STRS = list(info[1].keys())

    for i in range(0, len(info[0])):
        subsequence = STRS[i]
        count = longest_match(sequence, subsequence)
        counts[subsequence] = count
    counts_values = list(counts.values())

    # TODO: Check database for matching profiles
    for i in range(0, len(info)):
        matches = 0
        data_values = list(info[i].values())

        for j in range(0, len(info[0])):
            if data_values[j] == counts_values[j]:
                matches += 1
        if matches == len(info[0])-1:
            print(f"{data_values[0]}")
        else:
            print("No Match")
            sys.exit()


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
