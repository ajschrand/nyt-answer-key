# spacy only works with torch version <=2.2.2; 2.3 fails
import spacy

from collections import defaultdict
from more_itertools import distinct_combinations
from statistics import median
from utils.str_utils import get_list_grid
from colorama import Fore


class Grouping:
    def __init__(self, words, similarity):
        self.words = words
        self.similarity = similarity
        
    def __lt__(self, other):
        return self.similarity < other.similarity

    def __repr__(self):
        return f"{self.words} - {self.similarity}"
    
    def __str__(self) -> str:
        res = ""
        for i in range(len(self.words)):
            res += self.words[i]
            if i != len(self.words) - 1:
                res += " "
                
        return res


def play_connections():
    """
    Gets input of a connections game board followed by guesses.
    The board is a list of 16 words and the guesses are lists 
    of words and the number of those words properly grouped.

    "MGS" stands for "Median Grouping (semantic) Similarities"
    It is the metric for how good of a guess a grouping is.
    The higher the MGS, the better the guess.

    https://www.nytimes.com/games/connections
    """
    print("Enter the 16 words separated by spaces")
    word_list = input().split()

    all_groupings = distinct_combinations(word_list, 4)
    mgs = sorted(get_mgs(all_groupings), reverse=True)

    print(f"Suggested guess: {mgs[0].words}")
    print("Enter a guess with the number of known grouped items after it")
    print("in the format 'word1 word2 word3 word4;num_grouped'")
    guess_input = input()

    found_solutions = []
    while guess_input != "q":
        guess, num_grouped = process_guess_input(guess_input)
        if num_grouped == 4:
            found_solutions.append(guess)

        mgs = reduce_remaining_groupings(mgs, guess, num_grouped)
        if len(mgs) == 1:
            found_solutions.append(mgs[0])

        if len(found_solutions) < 4:
            if len(mgs) < 50:
                print("Remaining groupings:")
                print(get_list_grid(mgs, 1))
            else:
                print(f"{len(mgs)} groupings remaining")

            print(f"Suggested guess: {mgs[0].words}")
        else:
            print("Solution:")
            for grouping in found_solutions:
                print(grouping)
            break

        print("Enter a guess")
        guess_input = input()


def auto_connections(actual_solutions):
    """
    Plays the connections game automatically using the actual solutions as input

    Args:
        actual_solutions (List): A list of 4 lists of words representing the actual solutions
    """
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
    mgs = sorted(get_mgs(all_groupings), reverse=True)

    print(f"Solving board:")

    num_guesses = 0
    found_solutions = []
    while len(found_solutions) != 4:
        best_grouping = mgs[0].words
        num_grouped = get_num_grouped(best_grouping, len(found_solutions) == 2)
        if num_grouped == 4:
            found_solutions.append(best_grouping)

        num_guesses += 1

        color = Fore.GREEN if num_grouped == 4 else Fore.WHITE
        print(f"{color}Guess {num_guesses}: {best_grouping}{Fore.WHITE}")
        mgs = reduce_remaining_groupings(mgs, best_grouping, num_grouped)


def process_guess_input(guess_input):
    """
    Turns a raw guess string into a list of guessed words and
    its number of properly grouped words

    Args:
        guess_input (String): The raw guess input

    Returns:
        Tuple: A tuple containing the guessed words and the number of properly grouped words
    """
    guess, num_grouped = guess_input.split(";")
    guess = guess.split()
    num_grouped = int(num_grouped)
    return guess, num_grouped


def get_mgs(groupings, nlp=spacy.load("en_core_web_md")):
    """
    Calculates the median of the semantic similarities of all pairs of words
    in a grouping for all groupings in the input list

    Args:
        groupings (List): A list of groupings to calculate the median semantic similarity for

    Returns:
        Dict: The median semantic similarity for each grouping
    """
    mgs = []
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
        mgs.append(Grouping(grouping, median(grouping_similarities)))

    return mgs


def is_grouping_valid_for_guess(grouping, guess, num_grouped):
    """
    Determines if a grouping is valid for a given guess
    by checking the number of words in that grouping
    against the number of properly grouped words given in the clue

    Args:
        grouping (List): The grouping of words to check
        guess (List): The guessed words
        num_grouped (int): The number of properly grouped words given in the clue

    Returns:
        bool: True if the grouping is valid for the guess, False otherwise
    """
    count = 0
    for word in guess:
        if word in grouping.words:
            count += 1

    if num_grouped == 4:
        return count == 0
    elif num_grouped == 0:
        return count != 4 and count != 3
    else:
        return count == num_grouped or count == 4 - num_grouped or count == 0


def reduce_remaining_groupings(prev_remaining_groupings, guess, num_grouped):
    """
    Eliminates the groupings in the passed {grouping: similarity} dict
    that are not valid for the given guess

    Args:
        prev_remaining_groupings (Dict): A dictionary of groupings to their similarity values
        guess (List): The guessed words
        num_grouped (int): The number of properly grouped words in the guess

    Returns:
        Dict: The reduced dictionary of groupings that are valid with the given guess
    """
    cur_remaining_groupings = [
        grouping for grouping in prev_remaining_groupings 
        if is_grouping_valid_for_guess(grouping, guess, num_grouped)
    ]

    return cur_remaining_groupings


def is_grouping_valid_for_guess_info(grouping, guess_info):
    for guess in guess_info:
        if not is_grouping_valid_for_guess(grouping, guess['grouping'], guess['numGrouped']):
            return False
        
    return True


def find_best_guess_groupings(word_list, guess_info, nlp):
    import heapq
    
    g = get_mgs(distinct_combinations(word_list, 4), nlp)
    top_five_groupings = []
    heapq.heapify(top_five_groupings)
    
    for grouping in g:
        if not is_grouping_valid_for_guess_info(grouping, guess_info):
            continue
        
        if len(top_five_groupings) < 5:
            heapq.heappush(top_five_groupings, grouping)
        elif grouping.similarity > top_five_groupings[0].similarity:
            heapq.heappushpop(top_five_groupings, grouping)
        
    return [str(grouping) for grouping in heapq.nlargest(5, top_five_groupings)]

