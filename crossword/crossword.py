# For testing purposes
# Fixes the utils import to allow running the file directly instead of via main.py
# Remove when complete
# ------------------------------------------
from pathlib import Path
cwd = Path(__file__).resolve().parent
parent_dir = cwd.parent

import sys
sys.path.append(str(parent_dir))
# ------------------------------------------

import re
from utils import get_list_grid
from utils import get_english_words

class CrosswordBoard:
    def __init__(self, fen) -> None:
        self.board = self.process_fen(fen)
        self.iter_index = 0
        self.is_row_iterating = True
    
    def process_fen(self, fen):
        board = []
        for input_line in fen.split('/'):
            # Replace numbers with that many question marks
            output_line = re.sub(r'\d+', lambda m: '?' * int(m.group()), input_line)
            board.append(output_line)
            
        return board
    
    def get_row(self, index):
        return self.board[index]
    
    def set_row(self, index, row):
        self.board[index] = row
        
    def get_col(self, index):
        return "".join(row[index] for row in self.board)
    
    def set_col(self, index, col):
        for i, char in enumerate(col):
            self.board[index][i] = char
            
    def __str__(self) -> str:
        return get_list_grid(self.board, 1)
    
    def __iter__(self):
        self.is_row_iterating = True
        return self
    
    def __next__(self):
        if self.is_row_iterating:
            if self.iter_index < len(self.board):
                value = self.get_row(self.iter_index)
                self.iter_index += 1
                return value
            else:
                self.is_row_iterating = False
                self.iter_index = 0
            
        if self.iter_index >= len(self.board[0]):
            raise StopIteration
        
        value = self.get_col(self.iter_index)
        self.iter_index += 1
        
        return value


def play_crossword():
    print("Enter the shape FEN of the game board")
    print("Use letters for letters, '-' for black blocks,")
    print("numbers to represent the count of white blocks in a row, and slashes to go to the next line")
    
    fen = input()
    board = CrosswordBoard(fen)
    
    for clue in board:
        print(clue)
    
    print(board)
    

if __name__ == "__main__":
    play_crossword()