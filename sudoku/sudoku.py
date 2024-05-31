from colorama import Fore
from copy import deepcopy

class SudokuBoard:
    """
    Represents a Sudoku board and provides functionality to solve it.

    Attributes:
        initialBoard (list[list[int]]): The initial state of the Sudoku board.
        solvedBoard (list[list[int]]): A copy of the initial board, used to track the solution.

    Methods:
        solveSudoku(): Solves the Sudoku board using backtracking.
        solve(board, i=0, j=0): Recursive helper function for solveSudoku().
        __str__(): Returns a string representation of the solved board with color-coded values.
    """
    
    def __init__(self, board):
        """
        Initializes a SudokuBoard object.

        Args:
            board (list[list[int]]): A 9x9 2D list representing the initial Sudoku board.
        """
        self.initialBoard = board
        self.solvedBoard = deepcopy(board)  # Deep copy to avoid modifying original board

    def solveSudoku(self):
        """
        Solves the Sudoku board in place using backtracking.
        """
        self.solve(self.solvedBoard)

    def solve(self, board, i=0, j=0):
        """
        Recursive helper function to solve the Sudoku board using backtracking.

        Args:
            board (list[list[int]]): The current state of the board.
            i (int, optional): The current row index (default: 0).
            j (int, optional): The current column index (default: 0).

        Returns:
            bool: True if a solution is found, False otherwise.
        """
        def findNextCellToFill(board):
            for x in range(0, 9):
                for y in range(0, 9):
                    if board[x][y] == 0:
                        return x, y

            return -1, -1
        
        def isValid(board, i, j, e):
            rowOk = all([e != board[i][x] for x in range(9)])
            if not rowOk:
                return False

            columnOk = all([e != board[x][j] for x in range(9)])
            if not columnOk:
                return False

            # Gets the top left coordinates of the section containing the i,j cell
            squareTopX, squareTopY = 3 * (i//3), 3 * (j//3)
            for x in range(squareTopX, squareTopX + 3):
                for y in range(squareTopY, squareTopY + 3):
                    if board[x][y] == e:
                        return False

            return True
        
        i, j = findNextCellToFill(board)
        if i == -1:
            return True

        for e in range(1, 10):
            if isValid(board, i, j, e):
                board[i][j] = e
                if self.solve(board, i, j):
                    return True  # Solution found
                board[i][j] = 0  # Backtrack
                
        return False

    def __str__(self) -> str:
        """
        Returns a string representation of the solved Sudoku board, color-coding given and solved numbers.

        Returns:
            str: The color-coded string representation of the solved board.
        """
        board_str = ""
        for i, row in enumerate(self.solvedBoard):
            line = ""
            for j, num in enumerate(row):
                if self.initialBoard[i][j] == 0:
                    line += f"{Fore.GREEN}{num}{Fore.RESET} "
                else:
                    line += f"{num} "
            board_str += line + "\n"
        return board_str.strip()
    
    
def playSudoku():
    print("Enter the sudoku board one line at a time")
    
    board = []
    for _ in range(9):
        board.append([int(char) for char in input()])
    
    autoSudoku(board)


def autoSudoku(board):
    s = SudokuBoard(board)
    s.solveSudoku()
    print(s)