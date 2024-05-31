import os
import wordfreq as wf
import json

from statistics import median
from utils import wordContainsDuplicateLetters
from collections import defaultdict
from pathlib import Path
cwd = Path(__file__).resolve().parent

DEFAULT_STARTING_GUESS = "crate"

VALID_WORDLE_ANSWERS = []
with open(f"{cwd}\\wordle-answers-alphabetical.txt", 'r') as f:
    for line in f:
        VALID_WORDLE_ANSWERS.append(line.strip())

# Calculate the frequency of the appearance of each letter in the valid Wordle answers
# If the letter frequencies have already been calculated, load them from the file
# Otherwise, calculate them and save them to the file
LETTER_FREQUENCIES_ANSWERS = None
if os.path.exists(f"{cwd}\\letterFrequencies.txt"):
    LETTER_FREQUENCIES_ANSWERS = json.load(open(f"{cwd}\\letterFrequencies.txt", 'r'))
else:
    LETTER_FREQUENCIES_ANSWERS = defaultdict(lambda: defaultdict(int))
    for answer in VALID_WORDLE_ANSWERS:
        for i, letter in enumerate(answer):
            LETTER_FREQUENCIES_ANSWERS[str(i)][letter] += 1

    json.dump(LETTER_FREQUENCIES_ANSWERS, open(f"{cwd}\\letterFrequencies.txt", 'w'))


# Play Wordle manually
# Enter guesses followed by their info strings
# Enter "q" to quit
# Enter "r" to restart
def playWordle():
    print("Welcome to Wordle Solver!")
    print("Enter your guess followed by its info string.")

    guessString = input("Guess: ")
    guessInfo = {}
    while guessString != "q":
        guess, info = guessString.split()
        infoList = [int(info[i]) for i in range(5)]
        guessInfo[guess] = infoList

        possibleSolutions = generateWordleGuesses(guessInfo)
        if len(possibleSolutions) == 1:
            print(f"Solution: {possibleSolutions[0]}")
            break
        
        print(generateWordleGuesses(guessInfo)[:5])

        guessString = input("Guess: ")
        if guessString == "r":
            playWordle()
            return


# Automatically solve a Wordle word
# If printGuesses is True, print each guess as it is made
# Return the number of guesses required to solve the word
# If the word is not solved after 6 guesses, return 6
def autoWordle(wordToGuess, startingGuess=DEFAULT_STARTING_GUESS, printGuesses=False):
    guessInfo = {}
    numGuesses = 0
    optimizedRemainingWords = []
    while True:
        if numGuesses <= 1:
            optimizedRemainingWords = generateWordleGuesses(
                guessInfo, startingGuess=startingGuess)
        else:
            optimizedRemainingWords = generateWordleGuesses(
                guessInfo, startingGuess=startingGuess, remainingWords=optimizedRemainingWords)

        guess = optimizedRemainingWords[0]
        numGuesses += 1

        if printGuesses:
            print(guess)

        info = giveWordleClues(wordToGuess, guess)
        guessInfo[guess] = info

        if guess == wordToGuess or numGuesses == 6:
            if printGuesses:
                print(generateEmojiGuessSummary(guessInfo))
                
            return numGuesses


# Generate a Wordle guess based on the information gathered from previous guesses
# Find all possible words that match the information gathered so far
# Optimize the choice of word based on the information gathered so far and the current amount of information
# Return the first word in the optimized list of possible words
def generateWordleGuesses(guessInfo, startingGuess=DEFAULT_STARTING_GUESS, remainingWords=VALID_WORDLE_ANSWERS):
    if len(guessInfo) == 0:
        return [startingGuess]

    latestGuess = list(guessInfo.keys())[-1]
    numLettersFound = sum([1 for num in guessInfo[latestGuess] if num != 0])

    words = findPossibleWords(guessInfo, remainingWords=remainingWords)
    words = optimizeWordChoice(words, numLettersFound)

    return words


# Find all possible words that match the information gathered so far
def findPossibleWords(guessInfo, remainingWords=VALID_WORDLE_ANSWERS):
    # Helper functions for findPossibleWords
    # Check if the correct letters in a word match the correct letters in the guess
    def doCorrectLettersMatch(word, correctLetters):
        for i in range(5):
            if correctLetters[i] == '_':
                continue

            if word[i] != correctLetters[i]:
                return False
        return True

    # Helper functions for findPossibleWords
    # Check if the incorrect letters in a word match the incorrect letters in the guess
    def doIncorrectLettersMatch(word, incorrectLetters):
        for i, lettersList in enumerate(incorrectLetters):
            for letter in lettersList:
                if letter == word[i]:
                    return False
        return True

    # Helper functions for findPossibleWords
    # Check if the possible correct letter positions in a word match the possible correct letter positions in the guess
    def doPossibleCorrectLetterPositionsMatch(word, possibleCorrectLetterPositions):
        for letter in possibleCorrectLetterPositions:
            if word.find(letter) not in possibleCorrectLetterPositions[letter]:
                return False
        return True

    correctLetters = ["_"] * 5
    for guess in guessInfo:
        for i, info in enumerate(guessInfo[guess]):
            if info == 2:
                correctLetters[i] = guess[i]

    incorrectLetters = ["_"] * 5
    possibleCorrectLetterPositions = {}
    for guess in guessInfo:
        for i, info in enumerate(guessInfo[guess]):
            if info == 0:
                for j in range(5):
                    if guess[i] != correctLetters[j]:
                        incorrectLetters[j] += guess[i]
            elif info == 1:
                incorrectLetters[i] += guess[i]
                possibleIndexes = [j for j in range(5) if guess[i] not in incorrectLetters[j]]
                possibleCorrectLetterPositions[guess[i]] = possibleIndexes

    possibleWords = []
    for word in remainingWords:
        if not doCorrectLettersMatch(word, correctLetters):
            continue

        if not doIncorrectLettersMatch(word, incorrectLetters):
            continue

        if not doPossibleCorrectLetterPositionsMatch(word, possibleCorrectLetterPositions):
            continue

        possibleWords.append(word)

    return possibleWords


# Optimize the choice of word based on the information gathered so far and the current amount of information
# If the latest guess does not have much information, prioritize words with high letter frequencies
# If the latest guess has a lot of information, prioritize words with high word frequencies
def optimizeWordChoice(words, numLettersFound):
    optimized = []
    if numLettersFound < 3:
        optimized = sorted(words, key=assignLetterFrequencyScore, reverse=True)
    else:
        optimized = sorted(words, key=assignWordFrequencyScore, reverse=True)

    return optimized


# Assign a score to a word based on the frequency of its letters
# Used as a comparison function for sorting guesses
def assignLetterFrequencyScore(word):
    letterFrequencies = []
    for i, letter in enumerate(word):
        letterFrequencies.append(LETTER_FREQUENCIES_ANSWERS[str(i)][letter])
        
    wordScore = median(letterFrequencies)

    if wordContainsDuplicateLetters(word):
        wordScore *= 0.5

    return wordScore


# Assign a score to a word based on the frequency of the word itself
# Used as a comparison function for sorting guesses
def assignWordFrequencyScore(word):
    return wf.word_frequency(word, 'en')


# Builds an info list for a Wordle guess based on the word to guess and the guess itself
# The info list contains 0s, 1s, and 2s, where 0 indicates that the letter is not in the word to guess,
# 1 indicates that the letter is in the word to guess but not in the correct position, and 2 indicates
# that the letter is in the correct position
def giveWordleClues(wordToGuess, guess):
    wordList = list(wordToGuess)
    infoList = [0] * 5
    
    for i in range(5):
        if guess[i] == wordList[i]:
            infoList[i] = 2
            wordList[i] = "_"

    for i in range(5):
        if infoList[i] == 2:
            continue

        if guess[i] in wordList:
            infoList[i] = 1

    return infoList


def generateEmojiGuessSummary(guessInfo):
    guessInfoToEmoji = {0: "⬛", 1: "🟨", 2: "🟩"}
    
    summary = ""
    for guess in guessInfo:
        for num in guessInfo[guess]:
            summary += guessInfoToEmoji[num]
            
        summary += "\n"
            
    return summary