import sys
import csv


def main(seqstr, seqdna):

    # TODO: Check for command-line usage
    longest_str = {}

    fix = seqstr
    maxc = 0

    while fix in seqdna:
        maxc += 1
        fix += seqstr
    return maxc


if len(sys.argv) != 3:
    print("Usage: python dna.py database.csv sequence.txt")
    sys.exit(1)

    # TODO: Read database file into a variable

indivi = []
seqstr = []

sequence = sys.argv[1]

with open(sequence) as f:
    reader = csv.DictReader(f)
    for name in reader:
        indivi.append(name)

for i in dict.keys(indivi[0]):
    seqstr.append(i)
seqstr.pop(0)

# TODO: Read DNA sequence file into a variable

txtfile = open(sys.argv[2])
seqdna = txtfile.read()

# TODO: Find longest match of each STR in DNA sequence

countSTR = dict.fromkeys(seqstr, 0)

for i in range(len(seqstr)):
    x = main(seqstr[i], seqdna)
    countSTR[seqstr[i]] = x

# TODO: Check database for matching profiles

for i in range(len(indivi)):
    match = 0

    for j in range(len(seqstr)):
        if int(indivi[i][seqstr[j]]) == int(countSTR[seqstr[j]]):
            match += 1
            if match == len(seqstr):
                print(indivi[i]['name'])

                sys.exit()
        else:
            continue

print("No Match")


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

