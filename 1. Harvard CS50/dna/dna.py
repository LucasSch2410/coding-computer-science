import csv
import sys


def main():
    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Incorrect Usage of Command-Line Arguments.")
        sys.exit(1)

    csv_file_path = sys.argv[1]
    sequence_file_path = sys.argv[2]

    # TODO: Read database file into a variable
    database = []

    with open(csv_file_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            database.append(row)

    # TODO: Read DNA sequence file into a variable
    with open(sequence_file_path, "r") as sequence:
        dna_sequence = sequence.read()

    # TODO: Find longest match of each STR in DNA sequence
    subsequences = list(database[0].keys())[1:]
    subsequences_count = []

    for subsequence in subsequences:
        subsequences_count.append(longest_match(dna_sequence, subsequence))

    # TODO: Check database for matching profiles
    check_database(subsequences_count, database)


def check_database(subsequences_count, database):
    max_matches = 0
    winner = ""

    # Identify every person in database
    for person in database:
        matches = 0
        for i in range(len(person) - 1):
            dna = list(person.values())[i + 1]
            if int(dna) == subsequences_count[i]:
                matches += 1
        # If the matches in subsequence DNA is more than the maximum number
        # Of matches, put the person name in the winner string
        if matches > max_matches:
            max_matches = matches
            winner = person["name"]

    # Check to verify if the max_matches is considering all the subsequences
    if max_matches == len(subsequences_count):
        print(winner)
    else:
        print("No match")


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
