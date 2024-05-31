from utils import get_list_grid
from utils import word_has_all
from utils import get_english_words

def play_letter_boxed():
    print("Enter the letters one side at a time")
    print("A side e.g. 'abc'")
    
    board = []
    for _ in range(4):
        board.append([char.lower() for char in input()])
    
    auto_letter_boxed(board)


def auto_letter_boxed(board):
    board = [letter for letter in board]
    validWords = find_valid_words(board)
    
    one_word_solutions = find_one_word_solutions(board, validWords)
    two_word_solutions = find_two_word_solutions(board, validWords)
    two_word_solutions.sort(key=lambda x: len(x[0]) + len(x[1]))
    
    print(get_list_grid(one_word_solutions, 1))
    print(get_list_grid(two_word_solutions, 1))
    

def find_valid_words(board):
    letter_locations = {"": -1}
    for i, side in enumerate(board):
        for letter in side:
            letter_locations[letter] = i
    
    def is_word_valid(word):
        prevChar = ""
        for char in word:
            if char not in letter_locations:
                return False
            
            if letter_locations[char] == letter_locations[prevChar]:
                return False
            
            prevChar = char
            
        return True
    
    return [word for word in get_english_words() if is_word_valid(word)]     


def find_one_word_solutions(board, words):
    letters = [letter for side in board for letter in side]
    return [word for word in words if word_has_all(word, letters)]


def find_two_word_solutions(board, words):
    letters = [letter for side in board for letter in side]
    
    first_letter_to_word = {}
    for word in words:
        first_letter = word[0]
        if first_letter not in first_letter_to_word:
            first_letter_to_word[first_letter] = []
        
        first_letter_to_word[first_letter].append(word)
        
    solutions = []
    for first_word in words:
        last_letter = first_word[len(first_word) - 1]
        for second_word in first_letter_to_word[last_letter]:
            if word_has_all(first_word + second_word, letters):
                solutions.append((first_word, second_word))
            
    return solutions

