from collections import defaultdict

from utils.str_utils import get_list_grid
from utils.str_utils import word_has_all
from utils.str_utils import get_english_words

def play_letter_boxed():
    """
    Play a game of Letter Boxed by entering the board state
    """
    print("Enter the letters one side at a time")
    print("A side e.g. 'abc'")
    
    board = []
    for _ in range(4):
        board.append([char.lower() for char in input()])
    
    solutions = auto_letter_boxed(board)
    print(get_list_grid(solutions[:11], 1))


def auto_letter_boxed(board):
    """
    Automatically solve a game of Letter Boxed

    Args:
        board (List): A 4x3 2D list representing the Letter Boxed board
    """
    board = [[char.lower() for char in side] for side in board]
    validWords = find_valid_words(board)
    
    solutions = find_two_word_solutions(board, validWords)
    solutions.sort(key=lambda x: len(x[0]) + len(x[1]))
    
    return solutions
    

def find_valid_words(board):
    """
    Finds all valid words that can be made from the given board

    Args:
        board (List): A 4x3 2D list representing the Letter Boxed board

    Returns:
        List: A list of valid words that can be made from the board
    """
    letter_locations = {}
    for i, side in enumerate(board):
        for letter in side:
            letter_locations[letter] = i
    
    def is_word_valid(word):
        if word[0] not in letter_locations:
            return False
        
        prev_location = letter_locations[word[0]]
        for i in range(1, len(word)):
            if word[i] not in letter_locations:
                return False
            
            cur_location = letter_locations[word[i]]
            if prev_location == cur_location:
                return False
            
            prev_location = cur_location
            
        return True
    
    valid_words = [word for word in get_english_words() if is_word_valid(word)]
    return valid_words


def find_one_word_solutions(board, words):
    """
    Finds all one-word solutions that can be made from the given board

    Args:
        board (List): A 4x3 2D list representing the Letter Boxed board
        words (List): A list of valid words that can be made from the board

    Returns:
        List: A list of one-word solutions that can be made from the board
    """
    letters = [letter for side in board for letter in side]
    return [word for word in words if word_has_all(word, letters)]


def find_two_word_solutions(board, words):
    """
    Finds all two-word solutions that can be made from the given board

    Args:
        board (List): A 4x3 2D list representing the Letter Boxed board
        words (List): A list of valid words that can be made from the board

    Returns:
        List: A list of two-word solutions that can be made from the board
    """
    letters = {letter for side in board for letter in side}
    
    first_letter_to_sets_to_words = defaultdict(lambda: defaultdict(list))
    for word in words:
        first_letter_to_sets_to_words[word[0]][frozenset(word)].append(word)
        
    solutions = []
    for first_word in words:
        last_letter = first_word[-1]
        for second_word_set in first_letter_to_sets_to_words[last_letter]:
            if set(first_word).union(second_word_set) != letters:
                continue
            
            for second_word in first_letter_to_sets_to_words[last_letter][second_word_set]:
                solutions.append((first_word, second_word))
                
    return solutions

