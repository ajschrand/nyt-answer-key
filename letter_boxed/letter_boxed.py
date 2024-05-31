from utils import getCollectionAsGrid
from utils import wordContainsAllLetters
from utils import getAllEnglishWords

def playLetterBoxed():
    print("Enter the letters one side at a time")
    
    board = []
    for _ in range(4):
        board.append([char.lower() for char in input()])
    
    autoLetterBoxed(board)


def autoLetterBoxed(board):
    board = [letter.lower() for letter in board]
    validWords = findAllValidWords(board)
    
    oneWordSolutions = findOneWordSolutions(board, validWords)
    twoWordSolutions = findTwoWordSolutions(board, validWords)
    twoWordSolutions.sort(key=lambda x: len(x[0]) + len(x[1]))
    
    print(getCollectionAsGrid(oneWordSolutions, 1))
    print(getCollectionAsGrid(twoWordSolutions, 1))
    

def findAllValidWords(board):
    def isWordValid(letterLocations, word):
        prevChar = ""
        for char in word:
            if char not in letterLocations:
                return False
            
            if letterLocations[char] == letterLocations[prevChar]:
                return False
            
            prevChar = char
            
        return True
    
    letterLocations = {"": -1}
    for i, side in enumerate(board):
        for letter in side:
            letterLocations[letter] = i
    
    return [word for word in getAllEnglishWords() if isWordValid(letterLocations, word)]     


def findOneWordSolutions(board, words):
    letters = [letter for side in board for letter in side]
    return [word for word in words if wordContainsAllLetters(word, letters)]


def findTwoWordSolutions(board, words):
    letters = [letter for side in board for letter in side]
    
    firstLetterToWord = {}
    for word in words:
        firstLetter = word[0]
        if firstLetter not in firstLetterToWord:
            firstLetterToWord[firstLetter] = []
        
        firstLetterToWord[firstLetter].append(word)
        
    solutions = []
    for firstWord in words:
        lastLetter = firstWord[len(firstWord) - 1]
        for secondWord in firstLetterToWord[lastLetter]:
            if wordContainsAllLetters(firstWord + secondWord, letters):
                solutions.append((firstWord, secondWord))
            
    return solutions

