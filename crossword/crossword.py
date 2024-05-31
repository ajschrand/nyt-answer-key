# For testing purposes
# Fixes the utils import to allow running the file directly instead of via main.py
# Remove when complete
# ------------------------------------------
from pathlib import Path
cwd = Path(__file__).resolve().parent
parentDir = cwd.parent

import sys
sys.path.append(str(parentDir))
# ------------------------------------------

import re
from utils import getCollectionAsGrid
from utils import getAllEnglishWords

class CrosswordBoard:
    def __init__(self, fen) -> None:
        self.board = self.processBoardFEN(fen)
        self.iterIndex = 0
        self.isIteratingOverRows = True
    
    def processBoardFEN(self, fen):
        board = []
        for inputLine in fen.split('/'):
            outputLine = re.sub(r'\d+', lambda m: '?' * int(m.group()), inputLine)
            board.append(outputLine)
            
        return board
    
    def getRow(self, index):
        return self.board[index]
    
    def setRow(self, index, row):
        self.board[index] = row
        
    def getCol(self, index):
        return "".join(row[index] for row in self.board)
    
    def setCol(self, index, col):
        for i, char in enumerate(col):
            self.board[index][i] = char
            
    def __str__(self) -> str:
        return getCollectionAsGrid(self.board, 1)
    
    def __iter__(self):
        self.isIteratingOverRows = True
        return self
    
    def __next__(self):
        if self.isIteratingOverRows:
            if self.iterIndex < len(self.board):
                value = self.getRow(self.iterIndex)
                self.iterIndex += 1
                return value
            else:
                self.isIteratingOverRows = False
                self.iterIndex = 0
            
        if self.iterIndex >= len(self.board[0]):
            raise StopIteration
        
        value = self.getCol(self.iterIndex)
        self.iterIndex += 1
        
        return value


def playCrossword():
    print("Enter the shape FEN of the game board")
    print("Use letters for letters, '-' for black blocks,")
    print("numbers to represent the count of white blocks in a row, and slashes to go to the next line")
    
    fen = input()
    board = CrosswordBoard(fen)
    
    for clue in board:
        print(clue)
    
    print(board)
    

if __name__ == "__main__":
    playCrossword()