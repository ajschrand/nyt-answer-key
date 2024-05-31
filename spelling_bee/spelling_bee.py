"""
Spelling Bee Game Implementation

This module provides functions to simulate the New York Times Spelling Bee game.

Key Features:

* Finds all valid words given a set of letters and a mandatory "yellow letter".
* Filters words based on minimum length and allowed letter usage.
* Provides user interaction to play the game.
* Sorts answers by length for easy viewing.

Dependencies:

* utils.py: Contains helper functions `wordHasOnlyLetters` and `getAllEnglishWords`.
"""

from utils import wordHasOnlyLetters
from utils import getAllEnglishWords
from utils import wordContainsAllLetters

def playSpellingBee():
    """
    Starts the Spelling Bee game.

    Prompts the user for letters and the yellow letter.
    """
    print("Enter the letters")
    lettersList = input()
    
    print("Enter the yellow letter")
    yellowLetter = input()
    
    autoSpellingBee(yellowLetter, lettersList)
    

def autoSpellingBee(yellowLetter, lettersList):
    """
    Finds valid words for the Spelling Bee game.
    Prints valid words sorted by length.

    Args:
        yellowLetter: The mandatory letter that must be in each word.
        lettersList: The list of allowed letters.
    """
    
    def getPointValueForWord(word):
        """
        Gets the point value for valid words for the Spelling Bee game.
        
        4-letter words are worth 1 point each.
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
        
        bonus = 7 if wordContainsAllLetters(word, lettersList) else 0
        return len(word) + bonus
        
    answers = []
    for word in getAllEnglishWords():
        if len(word) < 4:
            continue

        if yellowLetter not in word:
            continue

        if not wordHasOnlyLetters(word, lettersList):
            continue

        answers.append(word)

    answers.sort(key=getPointValueForWord, reverse=True)
    print(answers)