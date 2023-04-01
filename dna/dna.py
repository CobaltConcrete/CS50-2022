import csv
import sys


def main():

    # TODO: Check for command-line usage

    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # TODO: Read database file into a variable

    database = []

    # open csvfile as LIST database[]
    with open(sys.argv[1], 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            database.append(row)

    # TODO: Read DNA sequence file into a variable

    # open sequence file
    with open(sys.argv[2], 'r') as seqfile:
        dna_sequence = seqfile.read()

    # TODO: Find longest match of each STR in DNA sequence

    # obtain subsequences as keys for DICT result{}, whose values are = longest_match(main_seq, sub_seq)
    result = {}
    subsequences = list(database[0].keys())[1:]
    for subsequence in subsequences:
        result[subsequence] = longest_match(dna_sequence, subsequence)

    # LIST database:
    # [{'name': 'Alpha',   'AGATC': 'number', 'AATG': 'number', 'TATC': 'number'},
    #  {'name': 'Bravo',   'AGATC': 'number', 'AATG': 'number', 'TATC': 'number'},
    #  {'name': 'Charlie', 'AGATC': 'number', 'AATG': 'number', 'TATC': 'number'}]

    # print(database[1]['name'])
    # Bravo

    # for person in database:
    #     print(person['name'])
    # Alpha
    # Bravo
    # Charlie

    # print(list(database[0].keys()))
    # ['name', 'AGATC', 'AATG', 'TATC']

    # print(list(result.keys()))
    # ['AGATC', 'AATG', 'TATC']

    # LIST subsequnces: ['AGATC', 'AATG', 'TATC']

    # DICT result: ['AGATC': number, 'AATG': number, 'TATC': number]

    # LIST person_tally.append(person[subsequence]): ['number', 'number', 'number']

    # LIST person_tally/sequence_tally:              [number, number, number]

    # TODO: Check database for matching profiles

    # obtain and compare a list of subsequences' values of each person against results'
    for person in database:
        person_values_str = list(person.values())[1:]
        person_values_int = [int(element) for element in person_values_str]

        result_values = list(result.values())

        if person_values_int == result_values:
            print(person['name'])
            return
    
    print('No match')


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
