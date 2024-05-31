# spacy only works with torch version <=2.2.2; 2.3 fails
import spacy

from collections import OrderedDict
from collections import defaultdict
from more_itertools import distinct_combinations
from statistics import median
from utils import get_list_grid
from colorama import Fore

# Takes as input a connections game board followed by guesses.
# The board is represented as a 16 length list of words,
# and the guesses are tuples with lists of words and the number of those words properly grouped.
#
# https://www.nytimes.com/games/connections
def play_connections():
    print("Enter the 16 words separated by spaces")
    word_list = input().split()

    all_groupings = distinct_combinations(word_list, 4)
    # "MGS" stands for "median grouping similarities"
    # It is the metric for how good of a guess a grouping is
    mgs = get_mgs(all_groupings)
    remaining_groupings = OrderedDict(
        sorted(mgs.items(), key=lambda x: x[1], reverse=True))

    # Get the first element from the dict of groupings sorted by median similarity
    best_grouping = next(iter(remaining_groupings))
    print(f"Suggested guess: {best_grouping}")

    print("Enter a guess with the number of known grouped items after it")
    print("in the format 'word1 word2 word3 word4;num_grouped'")
    guess_input = input()

    found_solutions = []
    while guess_input != "q":
        guess, num_grouped = process_guess_input(guess_input)
        if num_grouped == 4:
            found_solutions.append(guess)

        remaining_groupings = reduce_remaining_groupings(
            remaining_groupings, guess, num_grouped)
        if len(remaining_groupings) == 1:
            found_solutions.append(next(iter(remaining_groupings)))

        if len(found_solutions) < 4:
            if len(remaining_groupings) < 50:
                print("Remaining groupings:")
                print(get_list_grid(remaining_groupings, 1))
            else:
                print(f"{len(remaining_groupings)} groupings remaining")

            # Get the first element from the dict of groupings sorted by median similarity
            best_grouping = next(iter(remaining_groupings))
            print(f"Suggested guess: {best_grouping}")
        else:
            print("Solution:")
            for grouping in found_solutions:
                print(grouping)
            break

        print("Enter a guess")
        guess_input = input()


def auto_connections(actual_solutions):
    def get_num_grouped(guessed_grouping, eight_left):
        # Map to track guessed word appearance count by grouping index
        guess_locations = defaultdict(int)

        # Count guessed word appearance by grouping index
        for i, solution_grouping in enumerate(actual_solutions):
            for word in solution_grouping:
                if word in guessed_grouping:
                    guess_locations[i] += 1

        max_grouped = max(guess_locations.values())
        if (max_grouped in (3, 4)) or (max_grouped == 2 and eight_left):
            return max_grouped
        else:
            return 0

    word_list = [word for solution in actual_solutions for word in solution]
    all_groupings = distinct_combinations(word_list, 4)
    mgs = get_mgs(all_groupings)
    remaining_groupings = OrderedDict(
        sorted(mgs.items(), key=lambda x: x[1], reverse=True))

    print(f"Solving board:")

    num_guesses = 0
    found_solutions = []
    while len(found_solutions) != 4:
        # Get the most similar (first) element from the dict of groupings sorted by median similarity
        best_grouping = next(iter(remaining_groupings))
        num_grouped = get_num_grouped(best_grouping, len(found_solutions) == 2)
        if num_grouped == 4:
            found_solutions.append(best_grouping)

        num_guesses += 1

        color = Fore.GREEN if num_grouped == 4 else Fore.WHITE
        print(f"{color}Guess {num_guesses}: {best_grouping}{Fore.WHITE}")
        remaining_groupings = reduce_remaining_groupings(
            remaining_groupings, best_grouping, num_grouped)


# Turns a raw guess string into a list of guessed words and
# its number of properly grouped words
def process_guess_input(guess_input):
    guess, num_grouped = guess_input.split(";")
    guess = guess.split()
    num_grouped = int(num_grouped)
    return guess, num_grouped


# Calculates the median of the semantic similarities of all pairs of words
# in a grouping for all groupings in the input list
def get_mgs(groupings):
    nlp = spacy.load("en_core_web_md")

    mgs = {}
    # Cache for word pair similarities to mitigate duplicate calculations
    pair_similarities = {}
    for grouping in groupings:
        grouping_similarities = []
        # Get all pairs of words in the grouping
        pairs = distinct_combinations(grouping, 2)
        for pair in pairs:
            if pair not in pair_similarities:
                # Get semantic similarity using scapy library
                tokens = nlp(f"{pair[0]} {pair[1]}")
                similarity = tokens[0].similarity(tokens[1])

                # Add the similarity to the map to avoid duplicate calculations
                pair_similarities[pair] = similarity

            # Use a map to avoid expensive duplicate semantic similarity calculations
            grouping_similarities.append(pair_similarities[pair])

        # Add the median semantic similarity to the map
        mgs[grouping] = median(grouping_similarities)

    return mgs


# Eliminates the groupings in the passed {grouping: similarity} dict
# that are not valid for the given guess
def reduce_remaining_groupings(prev_remaining_groupings, guess, num_grouped):
    # Determines if a grouping is valid for a given guess
    # by checking the number of words in that grouping
    # against the number of properly grouped words given in the clue
    def is_grouping_valid(grouping, guess, num_grouped):
        count = 0
        for word in guess:
            if word in grouping:
                count += 1

        if num_grouped == 4:
            return count == 0
        elif num_grouped == 0:
            return count != 4 and count != 3
        else:
            return count == num_grouped or count == 4 - num_grouped or count == 0

    cur_remaining_groupings = OrderedDict()
    for grouping in prev_remaining_groupings:
        if is_grouping_valid(grouping, guess, num_grouped):
            cur_remaining_groupings[grouping] = prev_remaining_groupings[grouping]

    return cur_remaining_groupings
