# spacy only works with torch version <=2.2.2; 2.3 fails
import spacy

from collections import OrderedDict
from collections import defaultdict
from more_itertools import distinct_combinations
from statistics import median
from utils import getCollectionAsGrid
from colorama import Fore

# Takes as input a connections game board followed by guesses.
# The board is represented as a 16 length list of words,
# and the guesses are tuples with lists of words and the number of those words properly grouped.
#
# https://www.nytimes.com/games/connections
def playConnections():
    print("Enter the 16 words separated by spaces")
    wordList = input().split()
    
    possibleGroupings = distinct_combinations(wordList, 4)
    medianGroupingSimilarities = calculateMedianGroupingSimilarities(possibleGroupings)
    currRemaingingMGS = OrderedDict(
        sorted(medianGroupingSimilarities.items(), key=lambda x:x[1], reverse=True))
    
    # Get the first element from the dict of groupings sorted by median similarity
    bestGrouping = next(iter(currRemaingingMGS))
    print(f"Suggested guess: {bestGrouping}")
    
    print("Enter a guess with the number of known grouped items after it")
    rawGuess = input()
    
    solutions = []
    while rawGuess != "q":
        guess, numGrouped = processRawGuessInput(rawGuess)
        if numGrouped == 4:
            solutions.append(guess)
        
        currRemaingingMGS = reducePossibleGroupings(currRemaingingMGS, guess, numGrouped)
        if len(currRemaingingMGS) == 1:
            solutions.append(next(iter(currRemaingingMGS)))
        
        if len(solutions) < 4:
            if len(currRemaingingMGS) < 50:
                print("Remaining groupings:")
                print(getCollectionAsGrid(currRemaingingMGS, 1))
            else:
                print(f"{len(currRemaingingMGS)} groupings remaining")
                
            # Get the first element from the dict of groupings sorted by median similarity
            bestGrouping = next(iter(currRemaingingMGS))
            print(f"Suggested guess: {bestGrouping}")
        else:
            print("Solution:")
            for grouping in solutions:
                print(grouping)
            break
        
        print("Enter a guess with the number of known grouped items after it")
        rawGuess = input()
        
        
def autoConnections(actualSolutions):
    def determineNumGrouped(guessGrouping, actualSolutions, areEightWordsLeft):
        # Map to track guessed word appearance count by grouping index
        guessLocations = defaultdict(int)
        
        # Count guessed word appearance by grouping index
        for i, solutionGrouping in enumerate(actualSolutions):
            for word in solutionGrouping:
                if word in guessGrouping:
                    guessLocations[i] += 1
        
        maxGrouped = max(guessLocations.values())
        if (maxGrouped in (3, 4)) or (maxGrouped == 2 and areEightWordsLeft):
            return maxGrouped
        else:
            return 0
        
    wordList = [word for solution in actualSolutions for word in solution]
        
    print(f"Solving board:")
    # print(getCollectionAsGrid(wordList, 4))
    # print(f"For solution:")
    # print(getCollectionAsGrid(actualSolutions, 1))
    
    possibleGroupings = distinct_combinations(wordList, 4)
    medianGroupingSimilarities = calculateMedianGroupingSimilarities(possibleGroupings)
    currRemaingingMGS = OrderedDict(
        sorted(medianGroupingSimilarities.items(), key=lambda x:x[1], reverse=True))
    
    numGuesses = 0
    numCorrectGroupings = 0
    foundSolutions = []
    while numCorrectGroupings != 4:
        # Get the most similar (first) element from the dict of groupings sorted by median similarity
        bestGrouping = next(iter(currRemaingingMGS))
        numGuesses += 1
        
        numGrouped = determineNumGrouped(bestGrouping, actualSolutions, numCorrectGroupings == 2)
        if numGrouped == 4:
            numCorrectGroupings += 1
            foundSolutions.append(bestGrouping)
        
        color = Fore.GREEN if numGrouped == 4 else Fore.WHITE
        print(f"{color}Guess {numGuesses}: {bestGrouping}{Fore.WHITE}")
        currRemaingingMGS = reducePossibleGroupings(currRemaingingMGS, bestGrouping, numGrouped)
    
# Turns a raw guess string into a list of guessed words and 
# its number of properly grouped words
def processRawGuessInput(rawGuessInput):
    guess, numGrouped = rawGuessInput.split(";")
    guess = guess.split()
    numGrouped = int(numGrouped)
    return guess, numGrouped
    
# Calculates the median of the semantic similarities of all pairs of words
# in a grouping for all groupings in the input list
def calculateMedianGroupingSimilarities(groupings):
    nlp = spacy.load("en_core_web_md")
    
    medianGroupingSimilarities = {}
    # Cache for word pair similarities to mitigate duplicate calculations
    wordPairSimilarities = {}
    for grouping in groupings:
        groupingSimilarities = []
        # Get all pairs of words in the grouping
        pairs = distinct_combinations(grouping, 2)
        for pair in pairs:
            if pair not in wordPairSimilarities:
                # Get semantic similarity using scapy library
                tokens = nlp(f"{pair[0]} {pair[1]}")
                similarity = tokens[0].similarity(tokens[1])
                
                # Add the similarity to the map to avoid duplicate calculations
                wordPairSimilarities[pair] = similarity
                
            # Use a map to avoid expensive duplicate semantic similarity calculations
            groupingSimilarities.append(wordPairSimilarities[pair])
        
        # Add the median semantic similarity to the map
        medianGroupingSimilarities[grouping] = median(groupingSimilarities)
        
    return medianGroupingSimilarities

# Eliminates the groupings in the passed {grouping: similarity} dict
# that are not valid for the given guess
def reducePossibleGroupings(currRemaingingMGS, guess, numGrouped):
    # Determines if a grouping is valid for a given guess
    # by checking the number of words in that grouping
    # against the number of properly grouped words given in the clue
    def isGuessValidForGrouping(grouping, guess, numGrouped):
        count = 0
        for word in guess:
            if word in grouping:
                count += 1
                
        if numGrouped == 4:
            return count == 0
        elif numGrouped == 0:
            return count != 4 and count != 3
        else:
            return count == numGrouped or count == 4 - numGrouped or count == 0
    
    newRemainingMGS = OrderedDict()
    for grouping in currRemaingingMGS:
        if isGuessValidForGrouping(grouping, guess, numGrouped):
            newRemainingMGS[grouping] = currRemaingingMGS[grouping]
                
    return newRemainingMGS
    
    