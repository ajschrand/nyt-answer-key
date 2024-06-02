"""
Spelling Bee Game Implementation

This module provides functions to simulate the New York Times Spelling Bee game.

Key Features:

* Finds all valid words given a set of letters and a mandatory "yellow letter".
* Filters words based on minimum length and allowed letter usage.
* Provides user interaction to play the game.
* Sorts answers by length for easy viewing.

Dependencies:

* utils.py: Contains helper functions.
"""

from utils.str_utils import word_has_only
from utils.str_utils import word_has_all
from utils.str_utils import get_english_words

def play_spelling_bee():
    """
    Starts the Spelling Bee game.

    Prompts the user for letters and the yellow letter.
    """
    print("Enter the letters as one string (e.g. 'abcdefg')")
    letters_list = input()
    
    print("Enter the center (yellow) letter")
    center_letter = input()
    
    answers = auto_spelling_bee(center_letter, letters_list)
    print(answers)
    

def auto_spelling_bee(center_letter, letters_list):
    """
    Finds valid words for the Spelling Bee game.
    Prints valid words sorted by length.

    Args:
        yellowLetter: The mandatory letter that must be in each word.
        lettersList: The list of allowed letters.
        
    Returns:
        A list of valid words for the given puzzle.
    """
    
    def get_points(word):
        """
        Gets the point value for valid words for the Spelling Bee game.
        
        4-letter words are worth 1 point.
        Longer words earn 1 point per letter.
        Each puzzle includes at least one “pangram” which uses every letter.
        Pangrams are worth 1 point per letter plus 7 extra points.

        Args:
            word: The word to get the point value for
            
        Returns:
            The point value of the given word
        """
        if len(word) == 4:
            return 1
        
        bonus = 7 if word_has_all(word, letters_list) else 0
        return len(word) + bonus
        
    answers = []
    for word in get_english_words():
        if len(word) < 4:
            continue

        if center_letter not in word:
            continue

        if not word_has_only(word, letters_list):
            continue

        answers.append(word)

    answers.sort(key=get_points, reverse=True)
    return answers