import os
import wordfreq as wf
import json

from statistics import median
from utils import word_has_duplicates
from pathlib import Path
cwd = Path(__file__).resolve().parent

DEFAULT_STARTING_GUESS = "crate"
VALID_WORDLE_ANSWERS = json.load(open(f"{cwd}\\wordle_answers.txt", 'r'))
LETTER_FREQUENCIES_ANSWERS = json.load(open(f"{cwd}\\letter_frequencies.txt", 'r'))


# Play Wordle manually
# Enter guesses followed by their info strings
# Enter "q" to quit
# Enter "r" to restart
def play_wordle():
    print("Welcome to Wordle Solver!")
    print("Enter your guess followed by its info string.")
    print("An info string is a string of 0s, 1s, and 2s")
    print("where 0 = black, 1 = yellow, 2 = green")
    print("e.g. 'space 20212'")

    guess_str = input("Guess: ")
    guess_info = {}
    while guess_str != "q":
        guess, info = guess_str.split()
        info_list = [int(info[i]) for i in range(5)]
        guess_info[guess] = info_list

        solutions = generate_guesses(guess_info)
        if len(solutions) == 1:
            print(f"Solution: {solutions[0]}")
            break
        
        print(generate_guesses(guess_info)[:5])

        guess_str = input("Guess: ")
        if guess_str == "r":
            play_wordle()
            return


# Automatically solve a Wordle word
# If printGuesses is True, print each guess as it is made
# Return the number of guesses required to solve the word
# If the word is not solved after 6 guesses, return 6
def auto_wordle(wordle, start_guess=DEFAULT_STARTING_GUESS, print_guesses=False):
    guess_info = {}
    num_guesses = 0
    words = []
    while True:
        if num_guesses <= 1:
            words = generate_guesses(guess_info, start_guess=start_guess)
        else:
            words = generate_guesses(guess_info, start_guess=start_guess, words=words)

        guess = words[0]
        num_guesses += 1

        if print_guesses:
            print(guess)

        info = give_clues(wordle, guess)
        guess_info[guess] = info

        if guess == wordle or num_guesses == 6:
            if print_guesses:
                print(get_emoji_summary(guess_info))
                
            return num_guesses


# Generate a Wordle guess based on the information gathered from previous guesses
# Find all possible words that match the information gathered so far
# Optimize the choice of word based on the information gathered so far and the current amount of information
# Return the first word in the optimized list of possible words
def generate_guesses(guess_info, start_guess=DEFAULT_STARTING_GUESS, words=VALID_WORDLE_ANSWERS):
    if len(guess_info) == 0:
        return [start_guess]

    last_guess = list(guess_info.keys())[-1]
    letters_known = sum([1 for num in guess_info[last_guess] if num != 0])

    guesses = find_possible_words(guess_info, words=words)
    guesses = optimize_words(guesses, letters_known)

    return guesses


# Find all possible words that match the information gathered so far
def find_possible_words(guess_info, words=VALID_WORDLE_ANSWERS):
    # Helper functions for findPossibleWords
    # Check if the correct letters in a word match the correct letters in the guess
    def do_greens_match(word, greens):
        for i in range(5):
            if greens[i] == '_':
                continue

            if word[i] != greens[i]:
                return False
        return True

    # Helper functions for findPossibleWords
    # Check if the incorrect letters in a word match the incorrect letters in the guess
    def do_blacks_match(word, blacks):
        for i, letters_list in enumerate(blacks):
            for letter in letters_list:
                if letter == word[i]:
                    return False
        return True

    # Helper functions for findPossibleWords
    # Check if the possible correct letter positions in a word match the possible correct letter positions in the guess
    def do_yellows_match(word, yellows):
        for letter in yellows:
            if word.find(letter) not in yellows[letter]:
                return False
        return True

    greens = ["_"] * 5
    for guess in guess_info:
        for i, info in enumerate(guess_info[guess]):
            if info == 2:
                greens[i] = guess[i]

    blacks = ["_"] * 5
    yellows_positions = {}
    for guess in guess_info:
        for i, info in enumerate(guess_info[guess]):
            if info == 0:
                for j in range(5):
                    if guess[i] != greens[j]:
                        blacks[j] += guess[i]
            elif info == 1:
                blacks[i] += guess[i]
                possible_position = [j for j in range(5) if guess[i] not in blacks[j]]
                yellows_positions[guess[i]] = possible_position

    possible_words = []
    for word in words:
        if not do_greens_match(word, greens):
            continue

        if not do_blacks_match(word, blacks):
            continue

        if not do_yellows_match(word, yellows_positions):
            continue

        possible_words.append(word)

    return possible_words


# Optimize the choice of word based on the information gathered so far and the current amount of information
# If the latest guess does not have much information, prioritize words with high letter frequencies
# If the latest guess has a lot of information, prioritize words with high word frequencies
def optimize_words(words, letters_known):
    optimized = []
    if letters_known < 3:
        optimized = sorted(words, key=get_letter_freq, reverse=True)
    else:
        optimized = sorted(words, key=get_word_freq, reverse=True)

    return optimized


# Assign a score to a word based on the frequency of its letters
# Used as a comparison function for sorting guesses
def get_letter_freq(word):
    letter_frequencies = []
    for i, letter in enumerate(word):
        letter_frequencies.append(LETTER_FREQUENCIES_ANSWERS[str(i)][letter])
        
    score = median(letter_frequencies)

    if word_has_duplicates(word):
        score *= 0.5

    return score


# Assign a score to a word based on the frequency of the word itself
# Used as a comparison function for sorting guesses
def get_word_freq(word):
    return wf.word_frequency(word, 'en')


# Builds an info list for a Wordle guess based on the word to guess and the guess itself
# The info list contains 0s, 1s, and 2s, where 0 indicates that the letter is not in the word to guess,
# 1 indicates that the letter is in the word to guess but not in the correct position, and 2 indicates
# that the letter is in the correct position
def give_clues(wordle, guess):
    word_list = list(wordle)
    info_list = [0] * 5
    
    for i in range(5):
        if guess[i] == word_list[i]:
            info_list[i] = 2
            word_list[i] = "_"

    for i in range(5):
        if info_list[i] == 2:
            continue

        if guess[i] in word_list:
            info_list[i] = 1

    return info_list


def get_emoji_summary(guess_info):
    info_to_emoji = {0: "⬛", 1: "🟨", 2: "🟩"}
    
    summary = ""
    for guess in guess_info:
        for info in guess_info[guess]:
            summary += info_to_emoji[info]
            
        summary += "\n"
            
    return summary