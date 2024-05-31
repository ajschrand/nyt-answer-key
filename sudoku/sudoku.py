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
        self.initial_board = board
        self.solved_board = deepcopy(board)  # Deep copy to avoid modifying original board

    def solve_sudoku(self):
        """
        Solves the Sudoku board in place using backtracking.
        """
        self.solve(self.solved_board)

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
        def find_next_blank_Cell(board):
            for x in range(0, 9):
                for y in range(0, 9):
                    if board[x][y] == 0:
                        return x, y

            return -1, -1
        
        def is_valid_num(board, i, j, e):
            for x in range(9):
                if board[i][x] == e:
                    return False
            
            for x in range(9):
                if board[x][j] == e:
                    return False

            # Gets the top left coordinates of the section containing the i,j cell
            squareTopX, squareTopY = 3 * (i//3), 3 * (j//3)
            for x in range(squareTopX, squareTopX + 3):
                for y in range(squareTopY, squareTopY + 3):
                    if board[x][y] == e:
                        return False

            return True
        
        i, j = find_next_blank_Cell(board)
        if i == -1:
            return True

        for e in range(1, 10):
            if is_valid_num(board, i, j, e):
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
        for i, row in enumerate(self.solved_board):
            line = ""
            for j, num in enumerate(row):
                if self.initial_board[i][j] == 0:
                    line += f"{Fore.GREEN}{num}{Fore.RESET} "
                else:
                    line += f"{num} "
            board_str += line + "\n"
        return board_str.strip()
    
    
def play_sudoku():
    print("Enter the sudoku board one line at a time")
    print("A line e.g. '100030058'")
    
    board = []
    for _ in range(9):
        input_str = input()
        if input_str == "q":
            return
        
        board.append([int(char) for char in input_str])
    
    auto_sudoku(board)


def auto_sudoku(board):
    s = SudokuBoard(board)
    s.solve_sudoku()
    print(s)